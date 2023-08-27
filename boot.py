import network


#WIFI_SSID = "Will's WiFi"
#WIFI_PASSWORD = "FuckOffLMAO123!"

WIFI_SSID = "308 Negra Arroyo Lane"
WIFI_PASSWORD = "HooverMaxModel60"

# boot.py -- run on boot-up
print("boot.py -- run on boot-up")

# connect to WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Connected to WiFi:", wlan.ifconfig())

# Main loop
connect_to_wifi()