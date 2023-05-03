# -*- coding: utf-8 -*-
import time
import board
import keypad
import adafruit_ahtx0
import subprocess
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw, ImageFont

#*************************************************************
#     Get the current set temp
curr_set_temp = 0
with open("/home/pi/python/thermo/set_temp.txt", "r") as file:
    curr_set_temp = int(file.read())






#*************************************************************
#          functions to override the current temperature
#**************************************************************
def temp_up():
    print(f"Key {key_number} pressed.")
    save_new_temp(True)

def temp_down():
    print(f"Key {key_number} pressed.")
    save_new_temp(False)

def save_new_temp(direction):
     
    with open("/home/pi/python/thermo/set_temp.txt", "r") as file:
        curr_set_temp = int(file.read())

    if direction == True:
        curr_set_temp += 1
    else:
        curr_set_temp -= 1
        if curr_set_temp < 0:
            curr_set_temp = 0

    with open("/home/pi/python/thermo/set_temp.txt", "w") as out_file:
        out_file.write(str(curr_set_temp))
 
#***********************************************************************

#***********************************************************************
#   collect and display temperature and computer info on screen
#************************************************************************
def Collect_display_information():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    f,h = reset_temperature_humidity()

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    

    # Write text
    y = top
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]

    # temp and humidity
    f_text = "Temp is %3.2f" % f
    draw.text((x, y), f_text, font=font_big, fill="#FFFF00")
    y += font_big.getsize(f_text)[1]

    h_text = "RH is %3.2f" % h
    draw.text((x, y), h_text, font=font_big, fill="#00FF00")
    y += font_big.getsize(h_text)[1]

    
    #*************************************************************
#     Get the current set temp
    curr_set_temp = 0
    with open("/home/pi/python/thermo/set_temp.txt", "r") as file:
        curr_set_temp = int(file.read())

    draw.text((x,y), "   Temp set at   ", font=font, fill="#FFFFFF")
    y += font.getsize("   Temp set at   ")[1]
    draw.text((x,y),str(curr_set_temp), font=font_big, fill="#FFFF00")


    # Display image.
    display.image(image, rotation)
    return (f_text, h_text)
#************************************************************************

#*************************************************************************
#   Create sensor object, communicating over the board's 
#   default I2C bus and read temperature & humidity
#*************************************************************************
def reset_temperature_humidity():
    
    # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = adafruit_ahtx0.AHTx0(i2c)

    # write both to file
    f = (sensor.temperature * 1.8) + 32
    h = sensor.relative_humidity

    # write the values to disk
    with open("/home/pi/python/thermo/current_humidity.txt", "w") as h_file:
        h_file.write(str("Relative Humidity = {:.2f}".format(h)))
    with open("/home/pi/python/thermo/current_temp.txt", "w") as f_file:
        f_file.write(str("Temperature = {:.2f}".format(f)))
    
    return f, h



#***********************************************************************
#       set up the temperature override buttons and temperature module
#***********************************************************************
keys = keypad.Keys((board.D23,board.D24), value_when_pressed=False, pull=True)

# Create sensor object, communicating over the board's default I2C bus
f,h = reset_temperature_humidity()
#************************************************************************


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
display = st7789.ST7789(
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
height = display.width  # we swap height/width to rotate it to landscape!
width = display.height
image = Image.new("RGB", (width, height))
rotation = 0

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
#disp.image(image, rotation)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
display.image(image)

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



while True:
    
    #handle the button events
    event = keys.events.get()
    if event:
        key_number = event.key_number       
        if event.pressed and key_number == 1:
            temp_up()
        if event.pressed and key_number == 0:
            temp_down()
    
    # redraw the display
    Collect_display_information()


    
    
    #************************************
    # for debugging
    #************************************
    print("\nTemperature: %0.1f F" % f )
    print("Humidity: %0.1f %%" % h)
    #************************************


    time.sleep(1.5)



