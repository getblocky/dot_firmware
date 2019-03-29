          pulse = time_pulse_us(self.recv,state,200000)
                buffer.append(pulse)
                state = not state
            buffer.pop() 

            if len(buffer) < 20  or self._valid(buffer) == False :
                
                print("[InfraredRemote] Rejected" , len(buffer))
                led.fill((50,0,0));led.write()
                sleep_ms(100)
                led.fill((7,7,0));led.write()
                buffer = []
                continue

            # learnt , save
            print('[InfraredRemote] Learnt {} , length = {}'.format(name,len(buffer)))
            self._store(name,buffer)
            for i in range(0,255,10):
                led.fill((0,i,0));led.write()
                sleep_ms(10)
            for i in range(255,0,-10):
                led.fill((0,i,0));led.write()
                sleep_ms(10)
            led.fill((0,0,0));led.write()
            
            for i in range(3):
                led.fill((0,20,0));led.write()
        