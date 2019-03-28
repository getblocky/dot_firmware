lf,buffer):
        for i in buffer :
            if i < 200 :
                return False
        return True

    def _store(self,name,buffer):
        with open('IR/{}.bin'.format(name),'w') as fp :
            for i in buffer:
                fp.write(str(i))
                fp.write('\n')

    def _load(self,name):
        buffer = []
        with open('IR/{}.bin'.format(name)) as fp :
            for line in fp.readlines():
                buffer.append(int(line))
        return buffer

    def send(self,name):
        buffer = self._load(name)
        isMark = True
        for i in buffer:
            self.pwm.duty(512 if isMark else 0)
            sleep_us(i)
            isMark = not isMark
        self.pwm.duty(0)

