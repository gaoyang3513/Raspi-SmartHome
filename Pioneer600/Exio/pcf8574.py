#!/usr/bin/python
# -*- coding:utf-8 -*-

import pigpio
import RPi.GPIO as GPIO
import smbus
import time

class PCF8574(object):
	def __init__(self, bus, addr, irq, user_callbak, **kwargs) -> None:
		self.addr     = addr
		self.bus      = smbus.SMBus(bus)
		self.ports    = kwargs
		self.gpio_irq = irq
		self.callbak  = user_callbak
		self.pigpio   = pigpio.pi()

		i = 0
		port_val = 0
		for p in kwargs:
			if kwargs[p] == 1:
				port_val |= (1 << i)
			else :
				port_val &= ~(1 << i)
			i = i + 1
		self.bus.write_byte(self.addr, port_val)
		self.default = port_val

		#GPIO.setmode(GPIO.BCM)
		#GPIO.setup(irq, GPIO.IN, GPIO.PUD_UP)
		#GPIO.add_event_detect(irq, GPIO.FALLING, callback=self._press_handle, bouncetime=50)
#		self.cb1 = self.pigpio.callback(irq, pigpio.FALLING_EDGE, self._press_handle)

#	def _press_handle(self, gpio, level, tick):
#		print(gpio, level, tick)
		#port_val = self.bus.read_byte(self.addr)
#		print("port val: 0x%X" % port_val)
		#i = 0
		#press_keys = []
		#for p in self.ports:
		#	if port_val & (1 << i) == 0 :
		#		press_keys.append(p)
		#	i = i + 1
		#self.callbak(press_keys)
		#self.restore()

	def _get_val(self):
		port_val = self.bus.read_byte(self.addr)
		i = 0
		for p in self.ports:
			if port_val & (1 << i) :
				self.ports[p] = 1
			else :
				self.ports[p] = 0
			i = i + 1
	def _set_val(self):
		i = 0
		port_val = 0
		for p in self.ports:
			if self.ports[p] == 1:
				port_val |= (1 << i)
			else :
				port_val &= ~(1 << i)
			i = i + 1
		self.bus.write_byte(self.addr, port_val)
	def get_val(self, port):
		self._get_val()
		if port in self.ports :
			return self.ports.get(port)
	def set_val(self, port, val):
		if port in self.ports :
			if val != self.get_val(port) :
				self.ports[port] = val % 2
			self._set_val()
	def restore(self):
		self.bus.write_byte(self.addr, self.default)
	def get_keys(self):
		i = 0
		press_keys = []
		port_val = self.bus.read_byte(self.addr)
		for p in self.ports:
			if port_val & (1 << i) == 0 :
				press_keys.append(p)
			i = i + 1
		return press_keys

