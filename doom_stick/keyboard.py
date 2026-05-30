import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import led

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

def send_key(key):
    code = getattr(Keycode, key, None)
    keyboard.send(code)

def type_string(string, delay):
    for char in string:
        time.sleep(delay)
        layout.write(char)

def type_off(delay):
    for _ in range(5):
        send_key("ESCAPE")
        time.sleep(delay)
    send_key("GUI")
    for _ in range(5):
        send_key("TAB")
        time.sleep(delay)
    send_key("RIGHT_ARROW")
    time.sleep(delay)
    send_key("ENTER")
    time.sleep(delay)
    send_key("DOWN_ARROW")
    time.sleep(delay)
    send_key("DOWN_ARROW")
    time.sleep(delay)
    send_key("ENTER")
    led.turn_led("ON")