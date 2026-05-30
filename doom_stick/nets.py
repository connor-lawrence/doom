import time
import wifi

wifi_network = None
wifi_ip = None

networks = [
    # Add Wi-Fi networks here ("SSID", "PASSWORD")
]

def is_connected(): return wifi.radio.connected

def start_ap(ssid, password):
    wifi.radio.start_ap(ssid, password)
    global wifi_network, wifi_ip
    wifi_network = ssid
    wifi_ip = wifi.radio.ipv4_address_ap
    print("AP created (", ssid, ",", password, ")")

def connect_to(ssid, password):
    try:
        print("Connecting to", ssid, "with", password, "...")
        wifi.radio.connect(ssid, password)
        global wifi_network, wifi_ip
        wifi_network = ssid
        wifi_ip = wifi.radio.ipv4_address
        print("Successfully connected to", ssid)
        return True
    except Exception as error: 
        print("Error while connecting to", ssid, ":", error)
        return False

def connect_to_wifi():
    while True:
        for ssid, password in networks:
            if connect_to(ssid, password): return
        print("Retrying all networks...")
        time.sleep(1)