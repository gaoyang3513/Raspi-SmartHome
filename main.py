#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time
import RPi.GPIO as GPIO
import spidev as SPI
import Pioneer600.Led.led   as LED
import Pioneer600.Oled.oled as OLED
from PIL import Image,ImageDraw,ImageFont
import threading

# Raspberry Pi pin configuration:
LED_GPIO_RED  = 26

OLED_GPIO_RST = 19
OLED_GPIO_DC  = 16
OLED_SPI_BUS  = 0
OLED_SPI_CS   = 0

# 新线程执行的代码:
def blink_loop(*args, **kwargs):
	try:
		delay_ms = 500
		while True:
			GPIO.output(args, GPIO.HIGH)
			time.sleep(delay_ms/1000)
			GPIO.output(args, GPIO.LOW)
			time.sleep(delay_ms/1000)

	except:
		print("except")
		GPIO.output(args, GPIO.HIGH)
		GPIO.cleanup()

def main():
	led = LED.LED(LED_GPIO_RED)
	oled = OLED.OLED(OLED_GPIO_RST, OLED_GPIO_DC, OLED_SPI_BUS, OLED_SPI_CS)

	try:
		led_blink = threading.Thread(target=blink_loop, name='led_blink', args=(LED_GPIO_RED,))
		led_blink.start()

		oled.draw_text(0, 0, 16, 'Hello, workld')

		while True:
			time.sleep(1)

	except:
		print("Except")
		led_blink.join()

if __name__=='__main__':
    main()

