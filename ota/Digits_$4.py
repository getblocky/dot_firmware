turn _SEGMENTS[digit & 0x0f]

	def encode_string(self, string):
		"""Convert an up to 4 character length string containing 0-9, a-z,
		space, dash, star to an array of segments, matching the length of the
		source string."""
		segments = bytearray(len(string))
		for i in range(len(string)):
			segments[i] = self.encode_char(string[i])
		return segments

	def encode_char(self, char):
		"""Convert a character 0-9, a-z, space, dash or star to a segment."""
		o = ord(char)
		if o == 32:
			return _SEGMENTS[36] # space
		if o == 42:
			return _SEGMENTS[38] # star/degrees
		if o == 45:
			return _SEGMENTS[37] # dash
		if o >= 65 and o <= 90:
			return _SEGMENTS[o-55] # uppercase A-Z
		if o >= 97 and o <= 122:
			return _SEGMENTS[o-87] # lowercase a-z
		if o >= 48 and o <= 57:
			return _SEGMENTS[o-48] # 0-9
		raise ValueError("Character out of range: {:d} '{:s}'".format(o, chr(o)))

	def hex(self, val):
		"""Display a hex value 0x0000 through 0xffff, right aligned."""
		string = '{:04x}'.for