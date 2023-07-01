#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time
import RPi.GPIO as GPIO
import spidev as SPI
import Pioneer600.Led.LED      as LED
import Pioneer600.Oled.SSD1306 as SSD1306
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
LED_GPIO_RED  = 26

OLED_GPIO_RST = 19
OLED_GPIO_DC  = 16
OLED_SPI_BUS  = 0
OLED_SPI_CS   = 0

def main():

	# 128x64 display with hardware SPI:
	led  = LED.LED(LED_GPIO_RED)

	try:
		while True:
			time.sleep(1)
	except:
		print("except")

if __name__=='__main__':
    main()
