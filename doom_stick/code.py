import led
import nets
import server
import time
import keyboard

def blink_ip(ip):
    time.sleep(5)
    for i, part in enumerate(str(ip).split(".")):
        for chunk in part:
            led.blink_led(int(chunk), 0.15) if int(chunk) else led.blink_led(1, 1)
            time.sleep(1)
        time.sleep(2)

led.turn_led("OFF")
keyboard.type_off(0.5)
nets.start_ap("Doom_Stick", "stickofdoom")
time.sleep(1)
led.start_blink()
blink_ip(nets.wifi_ip)
led.start_blink()
server.open_server()