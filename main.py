#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time
import RPi.GPIO as GPIO
import spidev as SPI
import Pioneer600.Led.led       as LED
import Pioneer600.Oled.oled     as OLED
import Pioneer600.Sensor.bmp180 as BMP180
import Pioneer600.Exio.pcf8574  as PCF8574
from PIL import Image,ImageDraw,ImageFont
import threading
import socket

# Raspberry Pi pin configuration:
LED_GPIO_RED  = 26

IRQ_GPIO_PCF8764  = 21

OLED_GPIO_RST = 19
OLED_GPIO_DC  = 16
OLED_SPI_BUS  = 0
OLED_SPI_CS   = 0

# 获取本机ip地址
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

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
		GPIO.cleanup()

def joystick_callbak(kwargs):
#	print("Key val: %s" % kwargs)
	if 'KEY_A' in kwargs:
		print("Key A")
	elif 'KEY_B' in kwargs:
		print("Key B")
	elif 'KEY_C' in kwargs:
		print("Key C")
	elif 'KEY_D' in kwargs:
		print("Key D")

def main():
	bmp180 = BMP180.BMP180()
	led    = LED.LED(LED_GPIO_RED)
	oled   = OLED.OLED(OLED_GPIO_RST, OLED_GPIO_DC, OLED_SPI_BUS, OLED_SPI_CS)
	pcf875 = PCF8574.PCF8574(1, 0x20, 21, joystick_callbak, KEY_A=1, KEY_B=1, KEY_C=1, KEY_D=1, LED2=1, L3=0, L4=0, BUZZ=1)

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(IRQ_GPIO_PCF8764, GPIO.IN, GPIO.PUD_UP)
	GPIO.add_event_detect(IRQ_GPIO_PCF8764, GPIO.FALLING, bouncetime=100)

	try:
#		led_blink = threading.Thread(target=blink_loop, name='led_blink', args=(LED_GPIO_RED,))
#		led_blink.start()

		Raspi_IP = get_host_ip()
		oled.draw_text(0,  0, 14, 'Raspi-SmartHome')
		oled.draw_text(0, 16, 14, 'IP: %s' % Raspi_IP)

		while True:
			temperature = bmp180.read_temperature()
			pressure    = bmp180.read_pressure()
			oled.draw_rectangle(0, 32, 128, 64)
			oled.draw_text(0, 32, 14, u'温度: %.2f℃'  % temperature)
			oled.draw_text(0, 48, 14, u'气压: %.2fkPa' % (pressure/1000))

			if GPIO.event_detected(IRQ_GPIO_PCF8764):
				key  = ''
				keys = pcf875.get_keys()
				if 'KEY_A' in keys:
					key = 'A'
					print("Key A")
				elif 'KEY_B' in keys:
					key = 'B'
					print("Key B")
				elif 'KEY_C' in keys:
					key = 'C'
					print("Key C")
				elif 'KEY_D' in keys:
					key = 'D'
					print("Key D")
				GPIO.output(LED_GPIO_RED, 1)
				time.sleep(0.1)
				GPIO.output(LED_GPIO_RED, 0)
#				pcf875.set_val('BUZZ', 0)
#				time.sleep(0.1)
#				pcf875.set_val('BUZZ', 1)
#				oled.draw_rectangle(0, 16, 128, 32)
#				oled.draw_text(0, 16, 14, 'KEY: %s' % key)

			oled.flush()
			time.sleep(0.1)

	except:
		print("Except")
#		led_blink.join()

if __name__=='__main__':
    main()
