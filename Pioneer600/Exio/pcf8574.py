#!/usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import smbus
import time

class PCF8574(object):
	def __init__(self, bus, addr, kwargs, irq, callbak) -> None:
		self.addr    = addr
		self.bus     = smbus.SMBus(bus)
		self.ports   = kwargs

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

		self.irq = irq
		self.callbak = callbak

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(irq, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(irq, GPIO.FALLING, callback=self.__callbak, bouncetime=200)

	def __callbak(self, *args):
		port_val = self.bus.read_byte(self.addr)
		if self.callbak :
			self.callbak(port_val)

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

	def read(self):
		i = 0
		port_val = self.bus.read_byte(self.addr)
		for p in self.ports:
			if port_val & (1 << i) :
				self.ports[p] = 1
			else :
				self.ports[p] = 0
			i = i + 1
		return port_val


