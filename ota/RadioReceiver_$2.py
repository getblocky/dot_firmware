 self.rxRepeatCount = 0
            self.rxChangeCount = 0
        if self.rxChangeCount >= MAX_CHANGES :
            self.rxChangeCount = 0
            self.rxRepeatCount = 0
        self.rxTimings[self.rxChangeCount] = duration
        self.rxChangeCount += 1
        self.rxLastTimestamp = timestamp

    def rxWaveform(self,pnum,changeCount,timestamp):
        code = 0
        delay = self.rxTimings[0] // PROTOCOLS[pnum].sync_low
        delayTolerance = delay * self.rxTolerance // 100
        for i in range(1,changeCount,2):
            if abs(self.rxTimings[i]-delay*PROTOCOLS[pnum].zero_high < delayTolerance) and abs(self.rxTimings[i+1]-delay*PROTOCOLS[pnum].zero_low < delayTolerance):
                code <<= 1
            elif abs(self.rxTimings[i]-delay*PROTOCOLS[pnum].one_high < delayTolerance) and abs(self.rxTimings[i+1]-delay*PROTOCOLS[pnum].one_low < delayTolerance):
                code <<= 1
                code |= 1
            else :
                return False

       