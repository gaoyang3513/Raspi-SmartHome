import os
import sys
import time
import RPi.GPIO as GPIO
import spidev as SPI
sys.path.append(os.path.join(os.path.dirname(__file__),'Led'))
sys.path.append(os.path.join(os.path.dirname(__file__),'Oled'))
import Pioneer600.Led.LED      as LED
import Pioneer600.Oled.SSD1306 as SSD1306

from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
OLED_GPIO_RST = 19
OLED_GPIO_DC  = 16
OLED_SPI_BUS  = 0
OLED_SPI_CS   = 0

LED_GPIO_RED  = 26

# 128x64 display with hardware SPI:
disp = SSD1306.SSD1306(OLED_GPIO_RST, OLED_GPIO_DC, SPI.SpiDev(OLED_SPI_BUS, OLED_SPI_CS))

# 128x64 display with hardware SPI:
led  = LED.LED(LED_GPIO_RED)

def main():

	try:
		while True:
			time.sleep(1)
	except:
		print("except")

if __name__=='__main__':
    main()


