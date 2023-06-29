#!/usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

class LED(object):
	"""class for SSD1306  128*64 0.96inch OLED displays."""

	def __init__(self, led):
		LED = led

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(LED,GPIO.OUT)

		try:
			while True:
				GPIO.output(LED,GPIO.HIGH)
				time.sleep(1)
				GPIO.output(LED,GPIO.LOW)
				time.sleep(1)
		except:
			print("except")
			GPIO.output(LED,GPIO.HIGH)
			GPIO.cleanup()

