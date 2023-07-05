#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import spidev as SPI
from PIL import Image,ImageDraw,ImageFont
from . import SSD1306

# Raspberry Pi pin configuration:
OLED_GPIO_RST = 19
OLED_GPIO_DC  = 16
OLED_SPI_BUS  = 0
OLED_SPI_CS   = 0

OLED_WIDTH    = 128
OLED_HEIGHT   = 64

class OLED(object):
	"""class for OLED."""

	def __init__(self, gpio_rst=OLED_GPIO_RST, gpio_dc=OLED_GPIO_DC, spi_bus=OLED_SPI_BUS, spi_cs=OLED_SPI_CS):
		self.rst       = gpio_rst
		self.dc        = gpio_dc
		self.spi       = SPI.SpiDev(spi_bus, spi_cs)
		self.disp      = SSD1306.SSD1306(gpio_rst, gpio_dc, self.spi)
		self.disp.width  = OLED_WIDTH
		self.disp.height = OLED_HEIGHT

		# Load default font.
		self.font_size = 14
		self.font      = ImageFont.truetype(os.path.abspath('./Resource/Font/ZiTiGuanJiaFangSongTi-2.ttf'), self.font_size)

		disp = self.disp
		# Initialize library.
		disp.begin()

		# Clear display.
		disp.clear()
		disp.display()

		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		self.image = Image.new('1', (disp.width, disp.height))

		# Get drawing object to draw on image.
		self.draw = ImageDraw.Draw(self.image)

	def draw_rectangle(self, x, y, width, height):
		disp  = self.disp
		draw  = self.draw
		image = self.image

		# Draw a black filled box to clear the image.
		draw.rectangle((x, y, width, height), outline=0, fill=0)

	def draw_text(self, x, y, size, text):
		draw  = self.draw

		# Write two lines of text.
		draw.text((x, y), text, font=self.font, fill=255)

	def flush(self):
		disp  = self.disp
		image = self.image

		# Display image.
		disp.image(image)
		disp.display()
