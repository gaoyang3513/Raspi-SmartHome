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
		GPIO.output(args, GPIO.HIGH)
		GPIO.cleanup()

def main():
	bmp180 = BMP180.BMP180()
	led    = LED.LED(LED_GPIO_RED)
	oled   = OLED.OLED(OLED_GPIO_RST, OLED_GPIO_DC, OLED_SPI_BUS, OLED_SPI_CS)
	pcf875 = PCF8574.PCF8574(1, 32, KEY_A=1, KEY_B=1, KEY_C=1, KEY_D=1, LED2=1, L3=0, L4=0, BUZZ=1)

	try:
		led_blink = threading.Thread(target=blink_loop, name='led_blink', args=(LED_GPIO_RED,))
		led_blink.start()

		Raspi_IP = get_host_ip()
		oled.draw_text(0,  0, 14, 'Raspi-SmartHome')
		oled.draw_text(0, 16, 14, 'IP: %s' % Raspi_IP)

		while True:
			temperature = bmp180.read_temperature()
			pressure    = bmp180.read_pressure()
			oled.draw_rectangle(0, 32, 128, 64)
			oled.draw_text(0, 32, 14, u'温度: %.2f℃'  % temperature)
			oled.draw_text(0, 48, 14, u'气压: %.2fkPa' % (pressure/1000))
			oled.flush()

			pcf875.restore()
			is_key_up = pcf875.get_val('KEY_A')
			pcf875.set_val('LED2', is_key_up)
			print('Key A: %u' % is_key_up)

			time.sleep(1)

	except:
		print("Except")
		led_blink.join()

if __name__=='__main__':
    main()
