import time, network

wifi_ip = None

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
wlan_status = False

ap = network.WLAN(network.AP_IF)
ap.active(False)
ap_status = False

def create_ap(ssid, passwrd):
    global wifi_ip, ap_status
    ap.active(True)
    ap.config(essid=ssid, password=passwrd, authmode=network.AUTH_WPA_WPA2_PSK)
    print("AP created:", ssid, "(", passwrd, ")")
    wifi_ip = ap.ifconfig()[0]
    print("Connected at", wifi_ip)
    ap_status = True

def stop_ap():
    global wifi_ip, ap_status
    if ap.active(): ap.active(False)
    wifi_ip = None
    ap_status = False
    print("AP stopped")

def connect(ssid, password):
    global wifi_ip, wlan_status
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Connecting to", ssid, "with", password, "...")
    while not wlan.isconnected(): time.sleep(0.1)
    wifi_ip = wlan.ifconfig()[0]
    print("Connected at", wifi_ip)
    wlan_status = True

def disconnect():
    global wifi_ip, wlan_status
    if wlan.isconnected(): wlan.disconnect()
    wlan.active(False)
    wlan.active(True)
    wifi_ip = None
    wlan_status = False
    print("WiFi disconnected")