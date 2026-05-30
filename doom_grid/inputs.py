import time
from machine import Pin, ADC

back_button = Pin(5, Pin.IN, Pin.PULL_UP)
button_a = Pin(23, Pin.IN, Pin.PULL_UP)
button_b = Pin(18, Pin.IN, Pin.PULL_UP)
joy_up = Pin(35, Pin.IN, Pin.PULL_UP)
joy_down = Pin(34, Pin.IN, Pin.PULL_UP)
joy_left = Pin(26, Pin.IN, Pin.PULL_UP)
joy_right = Pin(25, Pin.IN, Pin.PULL_UP)
joy_click = Pin(27, Pin.IN, Pin.PULL_UP)
dial = ADC(Pin(36))

back_button_status = None
button_a_status = None
button_b_status = None
joy_up_status = None
joy_down_status = None
joy_left_status = None
joy_right_status = None
joy_click_status = None
dial_value = None

back_button_last = False
button_a_last = False
button_b_last = False
joy_up_last = False
joy_down_last = False
joy_left_last = False
joy_right_last = False
joy_click_last = False

back_button_just = False
button_a_just = False
button_b_just = False
joy_up_just = False
joy_down_just = False
joy_left_just = False
joy_right_just = False
joy_click_just = False

dial.atten(ADC.ATTN_11DB)
dial.width(ADC.WIDTH_12BIT)

def is_pressed(button): return button.value() == 0
def get_dial(dial): return dial.read()

def poll_loop():
    global back_button_status, back_button_last, back_button_just
    global button_a_status, button_a_last, button_a_just
    global button_b_status, button_b_last, button_b_just
    global joy_up_status, joy_up_last, joy_up_just
    global joy_down_status, joy_down_last, joy_down_just
    global joy_left_status, joy_left_last, joy_left_just
    global joy_right_status, joy_right_last, joy_right_just
    global joy_click_status, joy_click_last, joy_click_just
    global dial_value
    
    back_button_status = is_pressed(back_button)
    button_a_status = is_pressed(button_a)
    button_b_status = is_pressed(button_b)
    joy_up_status = is_pressed(joy_up)
    joy_down_status = is_pressed(joy_down)
    joy_left_status = is_pressed(joy_left)
    joy_right_status = is_pressed(joy_right)
    joy_click_status = is_pressed(joy_click)
    
    back_button_just = back_button_status and not back_button_last
    button_a_just = button_a_status and not button_a_last
    button_b_just = button_b_status and not button_b_last
    joy_up_just = joy_up_status and not joy_up_last
    joy_down_just = joy_down_status and not joy_down_last
    joy_left_just = joy_left_status and not joy_left_last
    joy_right_just = joy_right_status and not joy_right_last
    joy_click_just = joy_click_status and not joy_click_last
    
    back_button_last = back_button_status
    button_a_last = button_a_status
    button_b_last = button_b_status
    joy_up_last = joy_up_status
    joy_down_last = joy_down_status
    joy_left_last = joy_left_status
    joy_right_last = joy_right_status
    joy_click_last = joy_click_status
    
    dial_value = get_dial(dial)