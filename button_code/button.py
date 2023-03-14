# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import keypad


keys = keypad.Keys((board.D23,board.D24), value_when_pressed=False, pull=True)


while True:
    event = keys.events.get()
    
    # event will be None if nothing has happened.
    if event:
        key_number = event.key_number       
        if event.pressed:
            print(f"Key {key_number} pressed.")
        if event.released:
            print(f"Key {key_number} released.")
