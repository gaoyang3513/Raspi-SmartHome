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
GPIO_LED_RED    = 26
GPIO_PF8574_INT = 21

OLED_GPIO_RST = 19
OLED_GPIO_DC  = 16
OLED_SPI_BUS  = 0
OLED_SPI_CS   = 0

PCF8574_BUS_ID   = 1
PCF8574_BUS_ADDR = 0x20

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

pcf8574_in    = {'KEY_A':1, 'KEY_B':1, 'KEY_C':1, 'KEY_D':1}
pcf8574_out   = {'LED2':1,  'L3':0,    'L4':0,    'BUZZ':1}
pcf8574_ports = {**pcf8574_in, **pcf8574_out}

def pcf8574_callbak(*args, **kwargs) :
	print('Port val: %X' % args)
	GPIO.output(GPIO_LED_RED, 1)
	time.sleep(0.2)
	GPIO.output(GPIO_LED_RED, 0)

def main():
	bmp180 = BMP180.BMP180()
#	led    = LED.LED(GPIO_LED_RED)
	oled   = OLED.OLED(OLED_GPIO_RST, OLED_GPIO_DC, OLED_SPI_BUS, OLED_SPI_CS)
	pcf875 = PCF8574.PCF8574(PCF8574_BUS_ID, PCF8574_BUS_ADDR, pcf8574_ports, GPIO_PF8574_INT, pcf8574_callbak)

	GPIO.setup(GPIO_LED_RED, GPIO.OUT)

	try:
#		led_blink = threading.Thread(target=blink_loop, name='led_blink', args=(GPIO_LED_RED,))
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
			oled.flush()

			time.sleep(1)

	except:
		print("Except")
#		led_blink.join()

if __name__=='__main__':
    main()
