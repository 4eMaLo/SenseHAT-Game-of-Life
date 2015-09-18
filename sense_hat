''' Custom driver library for the SenseHAT
( I really disliked the fact you had to download huge libraries
just to install the official driver... )
'''


try:
	import smbus
except:
	raise Exception("This module requires smbus")

class LedMatrix:
	framebuffer = [0x00] * 192

	def __init__(self, address=0x46):
		self.ctrl_address = address
		self.i2cbus = smbus.SMBus(1)

	def clear(self):
		i = 0
		while i < 192:
			self.write_byte(i, 0)
			i += 1
		return False

	def set_pixel_fb(self, x, y, color):
		self.framebuffer[x*24+y   ] = color[0]
		self.framebuffer[x*24+y+8 ] = color[1]
		self.framebuffer[x*24+y+16] = color[2]
		return False

	def set_pixel_raw(self, x,y, color):
		''' Color is in the form ( RED, GREEN, BLUE ), where each value x is 0 <= x < 64 '''
		self.i2cbus.write_byte_data(self.ctrl_address, x*24+y, color[0])
		self.i2cbus.write_byte_data(self.ctrl_address, x*24+y+8, color[1])
		self.i2cbus.write_byte_data(self.ctrl_address, x*24+y+16, color[2])
		return False

	def fb_flush(self):
		i = 0
		while i < 192:
			self.i2cbus.write_byte_data(self.ctrl_address, i, self.framebuffer[i])
			i += 1
		return False


	def write_byte(self, addr, data):
		self.i2cbus.write_byte_data(self.ctrl_address, addr, data)
		return False
	def read_byte(self, addr):
		return self.i2cbus.read_byte_data(self.ctrl_address, addr)

class DPad:
	def __init__(self, address=0x46):
		self.ctrl_address = address
		self.i2cbus = smbus.SMBus(1)

	def get_state(self):
		joy = self.i2cbus.read_byte_data(self.ctrl_address, 0xF2)
		down = joy & 1 != 0
		right = joy & 0b10 != 0
		up = joy & 0b100 != 0
		left = joy & 0b10000 != 0
		push = joy & 0b1000 != 0

		return up, down, left, right, push
