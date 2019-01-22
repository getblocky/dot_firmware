from neopixel import NeoPixel
import sys
core = sys.modules['Blocky.Core']
class Indicator :
	def __init__ (self):
		self.animation = ''
		self.color = (0,0,0) # color that user set
		self.fcolor = [0,0,0] # color that the handler use
		self.rgb = NeoPixel(core.machine.Pin(5) , 12 , timing = True )
		self.speed = 0
		self.rgb.write()
		self.gap = 1
		self.running = 0

	async def heartbeat(self,color , speed , exit , gap = 1):
		return
		self.color = color
		self.speed = speed
		self.gap = gap
		self.running=1
		while  self.running == 1:
			r,g,b = self.rgb[0]
			if (r,g,b) == (0,0,0):	self.fcolor = self.color
			if (r,g,b) == self.fcolor:self.fcolor = (0,0,0)
			d,e,f = self.fcolor
			if (r<d): r = min(r + self.gap,d)
			if (r>d): r = max(r-self.gap,0)
			if (g<e): g = min(g + self.gap,e)
			if (g>e): g = max(g-self.gap,0)
			if (b<f): b = min(b + self.gap,f)
			if (b>f): b = max(b-self.gap,0)
			self.rgb.fill(   (r,g,b) )
			self.rgb.write()
			await core.wait(self.speed)
			if callab