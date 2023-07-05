#!/usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import smbus
import time

port_default = 0x0F

class PCF8574(object):
	def __init__(self, bus=1, addr=0x20) -> None:
		self.addr = 0x20
		self.bus  = smbus.SMBus(bus)
	def get_val(self, port):
		self.bus.read_byte(self.addr)
	def set_val(self, port, val):
		self.bus.write_byte(self.addr, val)
	def restore(self):
		self.bus.write_byte(self.addr, port_default)
