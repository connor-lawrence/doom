import time, neopixel
from machine import Pin

height = 8
width = 16

screen = neopixel.NeoPixel(Pin(4), height * width)

brightness = 1

def convert_xy(x, y): return y * width + x

def convert_brightness(raw): return min(int(raw * brightness), 255)

def clear(): screen.fill((0, 0, 0))

def set_led(x, y, r, g, b): screen[convert_xy(x, y)] = (convert_brightness(r), convert_brightness(g), convert_brightness(b))

def wipe(delay, r, g, b):
    for d in range(width + height - 1):
        for y in range(height):
            x = d - y
            if 0 <= x < width:
                i = y * width + x
                screen[i] = (convert_brightness(r), convert_brightness(g), convert_brightness(b))
        render()
        time.sleep(delay)

def render(): screen.write()