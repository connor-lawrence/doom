import time, screen, inputs, wifi, server

screen.clear()
screen.wipe(0.01, 10, 10, 10)
screen.wipe(0.01, 0, 0, 0)

dial_history = [0] * 5
row_brightness = [10, 7, 6, 5, 4]

timers = {}

now = time.ticks_ms()

def every(name, delay):
    global now
    now = time.ticks_ms()
    if name not in timers:
        timers[name] = now
        return True
    if time.ticks_diff(now, timers[name]) >= delay:
        timers[name] = now
        return True
    return False

while True:
    server.server_loop()
    inputs.poll_loop()
    
    for i in range(3):
        if server.bar == "red": screen.set_led(9 + i, 6, 10, 0, 0)
        elif server.bar == "yellow": screen.set_led(9 + i, 6, 10, 10, 0)
        elif server.bar == "green": screen.set_led(9 + i, 6, 0, 10, 0)
        elif server.bar == "cyan": screen.set_led(9 + i, 6, 0, 10, 10)
        elif server.bar == "blue": screen.set_led(9 + i, 6, 0, 0, 10)
        elif server.bar == "magenta": screen.set_led(9 + i, 6, 10, 0, 10)
        elif server.bar == "white": screen.set_led(9 + i, 6, 10, 10, 10)
        elif server.bar == "bright": screen.set_led(9 + i, 6, 255, 255, 255)
        elif server.bar == "off": screen.set_led(9 + i, 6, 0, 0, 0)
    
    if every("dial_timer", 100):
        for i in reversed(range(5)): dial_history[i] = dial_history[i - 1]
    dial_history[0] = inputs.dial_value
    
    for row in range(5):
        x = row_brightness[row]
        for i in range(16):
            if i < int(dial_history[row] // 256): screen.set_led(i, row, x, x, x)
            elif i == int(dial_history[row] // 256): screen.set_led(i, row, 0, ((dial_history[row] % 256) * x // 256), 0)
            else: screen.set_led(i, row, 0, 0, 0)
    
    screen.set_led(14, 6, 0, 10, 0) if inputs.back_button_status else screen.set_led(14, 6, 10, 10, 10)
    screen.set_led(13, 7, 0, 10, 0) if inputs.button_a_status else screen.set_led(13, 7, 10, 10, 10)
    screen.set_led(15, 7, 0, 10, 0) if inputs.button_b_status else screen.set_led(15, 7, 10, 10, 10)
    screen.set_led(1, 5, 0, 10, 0) if inputs.joy_up_status else screen.set_led(1, 5, 10, 10, 10)
    screen.set_led(1, 7, 0, 10, 0) if inputs.joy_down_status else screen.set_led(1, 7, 10, 10, 10)
    screen.set_led(0, 6, 0, 10, 0) if inputs.joy_left_status else screen.set_led(0, 6, 10, 10, 10)
    screen.set_led(2, 6, 0, 10, 0) if inputs.joy_right_status else screen.set_led(2, 6, 10, 10, 10)
    screen.set_led(1, 6, 0, 10, 0) if inputs.joy_click_status else screen.set_led(1, 6, 10, 10, 10)
    
    if inputs.button_a_just:
        if not wifi.ap_status: wifi.create_ap("Doom_Grid", "gridofdoom")
        elif wifi.ap_status: wifi.stop_ap()
    if inputs.button_b_just:
        if not server.server_status: server.host()
        elif server.server_status: server.close(server.server)
    
    screen.set_led(4, 6, 0, 0, 10)
    if wifi.ap_status: screen.set_led(5, 6, 0, 10, 0)
    else: screen.set_led(5, 6, 10, 10, 0)
    screen.set_led(6, 6, 10, 0, 0)
    if server.server_status: screen.set_led(7, 6, 0, 10, 0)
    else: screen.set_led(7, 6, 10, 10, 0)
    
    if inputs.joy_up_just and screen.brightness < 5: screen.brightness *= 1.5
    if inputs.joy_down_just and screen.brightness > 0.5: screen.brightness /= 1.5
    if inputs.joy_click_just: screen.brightness = 1
    
    server.server_loop()
    
    screen.render()