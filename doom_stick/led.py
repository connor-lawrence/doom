import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False
state = "OFF"

def turn_led(value):
    global state
    if value == "ON":
        led.value = True
        state = "ON"
    elif value == "OFF":
        led.value = False
        state = "OFF"

def blink_led(n, delay):
    for _ in range(n):
        turn_led("ON")
        time.sleep(delay)
        turn_led("OFF")
        time.sleep(delay)

def start_blink():
    blink_led(1, 0.5)
    blink_led(3, 0.1)