#!/usr/bin/python
# -*- coding:utf-8 -*-

from smbus2 import SMBus
import time

class AHT10:
	"""Interface library for AHT10/AHT20 temperature+humidity sensors"""

	AHTX0_I2CADDR_DEFAULT   = 0x38  # Default I2C address
	AHTX0_CMD_INITIALIZE    = 0xE1  # Initialization command
	AHTX0_CMD_TRIGGER       = 0xAC  # Trigger reading command
	AHTX0_CMD_SOFTRESET     = 0xBA  # Soft reset command
	AHTX0_STATUS_BUSY       = 0x80  # Status bit for busy
	AHTX0_STATUS_CALIBRATED = 0x08  # Status bit for calibrated

	def __init__(self, i2c, address=AHTX0_I2CADDR_DEFAULT):
		self._i2c     = SMBus(i2c)
		self._address = address
		self._buf     = bytearray(6)

		#cmd = [self.AHTX0_CMD_INITIALIZE, 0x08, 0x00]
		#for c in cmd :
		#	self._i2c.write_byte(self._address, c)
		#time.sleep(0.5)
		#self._i2c.read_byte(self._address)
		config = [0x08, 0x00]
		self._i2c.write_i2c_block_data(0x38, 0xE1, config)
		time.sleep(0.5)
		self._i2c.read_byte(0x38)
	def __read(self):
		#cmd = [self.AHTX0_CMD_TRIGGER, 0x33, 0x00]
		#for c in cmd :
		#	self._i2c.write_byte(self._address, c)
		#time.sleep(0.5)
		#for i in range(6):
		#	self._buf[i] = self._i2c.read_byte(self._address)
		#print('Read data: %s' % self._buf)
		MeasureCmd = [0x33, 0x00]
		self._i2c.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
		time.sleep(0.5)
		self._buf = self._i2c.read_i2c_block_data(0x38,0x00,len(self._buf))
	def temperature(self):
		self.__read()
		#temp = ((self._buf[3] & 0x0F) << 16) | (self._buf[4] << 8) | self._buf[5]
		#return ((temp*200) / 1048576) - 50
		temp = ((self._buf[3] & 0x0F) << 16) | (self._buf[4] << 8) | self._buf[5]
		return ((temp*200) / 1048576) - 50
	def relative_humidity(self):
		self.__read()
		#temp = ((self._buf[1] << 16) | (self._buf[2] << 8) | self._buf[3]) >> 4
		#return (temp * 100 / 1048576)
		temp = ((self._buf[1] << 16) | (self._buf[2] << 8) | self._buf[3]) >> 4
		return (temp * 100 / 1048576)
