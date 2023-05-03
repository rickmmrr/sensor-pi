# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import adafruit_ahtx0

#for server
from bottle import route, run, template
from datetime import datetime

#global
temp = str("")
rh = str()

curr_set_temp = 0

#get the current temperature setting
#******************************************
with open("/home/pi/python/thermo/set_temp.txt", "r") as file:
    curr_set_temp = int(str(file.read()))
#********************************************





#**************************************************************
#           Bottle module server setup
#***************************************************************
@route("/")
def index():
    temp, rh = collectdisplayinfo()
    dt = datetime.now()
    time = "{:%Y-%m-%d %H:%M:%S}".format(dt)
    return template("<b>{{f}} {{r}} : {{d}}</b>", d=time, 
                    f=temp, r=rh)
#*******************************************************************



#***********************************************************************
#   collect and display temperature and computer info on screen
#************************************************************************
def collectdisplayinfo():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    

    # Write text
    y = top
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]

    # temp and himidity
    f_text = "Temp is %3.2f" % f
    draw.text((x, y), f_text, font=font_big, fill="#FFFF00")
    y += font_big.getsize(f_text)[1]

    h_text = "RH is %3.2f" % h
    draw.text((x, y), h_text, font=font_big, fill="#00FF00")
    y += font_big.getsize(h_text)[1]

    draw.text((x,y), "   Temp set at   ", font=font, fill="#FFFFFF")
    y += font.getsize("   Temp set at   ")[1]
    draw.text((x,y),str(curr_set_temp), font=font_big, fill="#FFFF00")


    # Display image.
    disp.image(image, rotation)
    return (f_text, h_text)
#************************************************************************



# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_ahtx0.AHTx0(i2c)

f = (sensor.temperature * 1.8) + 32
h = sensor.relative_humidity

#*********************************************************
#       Setup the RGB display
#*********************************************************

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
    rotation=0,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 0

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
#disp.image(image, rotation)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
#*************************************************************************************

temp, rh = collectdisplayinfo()

run(host="0.0.0.0", port=8080, debug=True)
