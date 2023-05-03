import time
import board
import keypad
import adafruit_ahtx0
import os


def temp_up():
    print(f"Key {key_number} pressed.")
    save_new_temp(True)



def temp_down():
    print(f"Key {key_number} pressed.")
    save_new_temp(False)


def save_new_temp(direction):
    #update the current temp
    #******************************************
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(BASE_DIR + "/set_temp.txt", "r") as file:
        curr_set_temp = int(str(file.read()))
    if direction == True:
        curr_set_temp += curr_set_temp
    else:
        curr_set_temp -= curr_set_temp
    with open(os.join([BASE_DIR,"set_temp.txt"]), "w") as out_file:
        out_file.write(curr_set_temp)
    #********************************************




#set up the butons
keys = keypad.Keys((board.D23,board.D24), value_when_pressed=False, pull=True)


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

f = (sensor.temperature * 1.8) + 32

while True:
    
    #handle the button events
    event = keys.events.get()
    if event:
        key_number = event.key_number       
        if event.pressed and key_number == 1:
            temp_up()
        else:
            temp_down()


    #get the temp and Humidity
    print("\nTemperature: %0.1f F" % f )
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    time.sleep(2)



