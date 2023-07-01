#!/usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

class LED(object):
	"""class for LED."""

	def __init__(self, led):
		LED = led

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(LED,GPIO.OUT)
