import spidev as SPI
import SSD1306
import time

from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
GPIO_RST = 19
GPIO_DC  = 16
SPI_BUS = 0
SPI_CS  = 0

# 128x64 display with hardware SPI:
disp = SSD1306.SSD1306(GPIO_RST, GPIO_DC, SPI.SpiDev(SPI_BUS, SPI_CS))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width  = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 20

top    = padding
bottom = height - padding

# Move left to right keeping track of the current x position for drawing shapes.
x = padding
y = top

# Load default font.
font = ImageFont.load_default()

# Write two lines of text.
draw.text((x, y), 'Hello, world',  font=font, fill=255)

# Display image.
disp.image(image)
disp.display()
