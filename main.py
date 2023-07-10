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
import aht10 as AHT10

# Raspberry Pi pin configuration:
GPIO_LED_RED    = 26
GPIO_PF8574_INT = 21

OLED_GPIO_RST = 19
OLED_GPIO_DC  = 16
OLED_SPI_BUS  = 0
OLED_SPI_CS   = 0

PCF8574_BUS_ID   = 1
PCF8574_BUS_ADDR = 0x20

pcf8574_in    = {'KEY_L':1, 'KEY_U':1, 'KEY_D':1, 'KEY_R':1}
pcf8574_out   = {'LED2':1,  'L3':0,    'L4':0,    'BUZZ':1}
pcf8574_ports = {**pcf8574_in, **pcf8574_out}
key_lock = threading.Lock()

AHT10_BUS_ID   = 1

def pcf8574_callbak(port_val) :
	global press_keys
	global key_lock
	#print('Port val: %X' % port_val)

	key_lock.acquire()
	i = 0
	for p in pcf8574_ports :
		if (p in pcf8574_in) :
			if port_val & (1 << i) == 0 :
				press_keys.append(p)
		i = i + 1
	key_lock.release()

	GPIO.output(GPIO_LED_RED, 1)
	time.sleep(0.2)
	GPIO.output(GPIO_LED_RED, 0)

def menu_network(press_keys):
	global menu_page

	menu_item = 0
	if 'KEY_L' in press_keys :
		menu_page = (menu_page - 1) % len(menu_list)
	if 'KEY_R' in press_keys :
		menu_page = (menu_page + 1) % len(menu_list)
	if 'KEY_U' in press_keys :
		if menu_item :
			menu_item = menu_item - 1
	if 'KEY_D' in press_keys :
		menu_item = menu_item + 1

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()

	oled.draw_rectangle(0, 16, 128, 64)
	oled.draw_text(0, 16, 14, 'IP: %s' % ip)
	oled.flush()

def menu_main(press_keys):
	global menu_page

	menu_item = 0
	if 'KEY_L' in press_keys :
		menu_page = (menu_page - 1) % len(menu_list)
	if 'KEY_R' in press_keys :
		menu_page = (menu_page + 1) % len(menu_list)
	if 'KEY_U' in press_keys :
		if menu_item :
			menu_item = menu_item - 1
	if 'KEY_D' in press_keys :
		menu_item = menu_item + 1

#	temperature = bmp180.read_temperature()
#	pressure    = bmp180.read_pressure()
#	oled.draw_text(0, 32, 14, u'气压: %.2fkPa' % (pressure/1000))

	temperature = aht10.temperature()
	humidity    = aht10.relative_humidity()
	oled.draw_rectangle(0, 16, 128, 64)
	oled.draw_text(0, 16, 14, u'温度: %.1f℃' % temperature)
	oled.draw_text(0, 32, 14, u'湿度: %.1f%%'   % humidity)
	oled.flush()

#bmp180 = BMP180.BMP180()
oled   = OLED.OLED(OLED_GPIO_RST, OLED_GPIO_DC, OLED_SPI_BUS, OLED_SPI_CS)
pcf875 = PCF8574.PCF8574(PCF8574_BUS_ID, PCF8574_BUS_ADDR, pcf8574_ports, GPIO_PF8574_INT, pcf8574_callbak)
aht10  = AHT10.AHT10(AHT10_BUS_ID)

menu_page = 0
press_keys = []
menu_list = [['main', menu_main], ['network', menu_network]]

def main():
	global press_keys
	global menu_list
	global key_lock

	GPIO.setup(GPIO_LED_RED, GPIO.OUT)

	oled.draw_text(0,  0, 14, 'Raspi-SmartHome')
	oled.flush()

	print('Menu list size: %u' % len(menu_list))

	while True:
		key_lock.acquire()
		menu_list[menu_page][1](press_keys)
		press_keys = []
		key_lock.release()

		time.sleep(0.2)

if __name__=='__main__':
    main()
