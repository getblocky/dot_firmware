ide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return int(cms)

    def getDistance(self,unit='cm'):
        if unit == 'cm':
            return self.distance_cm()
        if unit == 'mm':
            return self.distance_mm()
        else :
            return 0
    
    def deinit(self):
        Pin(self.p[0],Pin.IN)