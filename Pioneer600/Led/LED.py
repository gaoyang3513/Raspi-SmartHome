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

LED_GPIO_RED  = 26

def main():
	# 128x64 display with hardware SPI:
	led  = LED.LED(LED_GPIO_RED)

if __name__=='__main__':
    main()
