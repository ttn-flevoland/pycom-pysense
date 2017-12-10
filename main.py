from settings import app_eui, app_key
from network import LoRa
from pysense import Pysense

import socket
import time
import pycom
import struct
import binascii

from lib.MPL3115A2 import MPL3115A2
from lib.LTR329ALS01 import LTR329ALS01
from lib.SI7006A20 import SI7006A20
from lib.LIS2HH12 import LIS2HH12

pycom.heartbeat(False)
pycom.rgbled(0x000000)

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, adr=True)

# Retrieve the dev_eui from the LoRa chip (Only needed for OTAA to retrieve once)
dev_eui = binascii.hexlify(lora.mac()).upper().decode('utf-8')

# Join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
count = 0
while not lora.has_joined():
    pycom.rgbled(0xffa500)
    time.sleep(0.2)
    pycom.rgbled(0x000000)
    time.sleep(2)
    print("Not yet joined count is:" ,  count)
    count = count + 1

# Show that LoRa OTAA has been succesfull
pycom.rgbled(0x0000ff)
time.sleep(0.5)
pycom.rgbled(0x000000)
time.sleep(0.1)
pycom.rgbled(0x0000ff)
time.sleep(0.5)
pycom.rgbled(0x000000)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# Set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# make the socket non-blocking
s.setblocking(False)

# Init the libraries
pysense = Pysense()
mpl3115a2 = MPL3115A2() # Barometric Pressure Sensor with Altimeter
ltr329als01 = LTR329ALS01() # Digital Ambient Light Sensor
si7006a20 = SI7006A20() # Humidity and Temperature sensor
lis2hh12 = LIS2HH12() # 3-Axis Accelerometer

while True:

    print(int(ltr329als01.light()[0] * 100))

    clean_bytes = struct.pack(">iiiiiii",
        int(mpl3115a2.temperature() * 100), # Temperature in celcius
        int(mpl3115a2.pressure() * 100), # Atmospheric pressure in bar
        int(ltr329als01.light()[0] * 100), # Light in lux
        int(si7006a20.humidity() * 100), # Humidity in percentages
        int(lis2hh12.roll() * 100), # Roll in degrees in the range -180 to 180
        int(lis2hh12.pitch() * 100), # Pitch in degrees in the range -90 to 90
        int(pysense.read_battery_voltage() * 100)) # Battery voltage

    # send the data over LPWAN network
    s.send(clean_bytes)
    # print(struct.unpack(">iiiiiii", clean_bytes))

    pycom.rgbled(0x007f00)
    time.sleep(0.2)
    pycom.rgbled(0x000000)
    time.sleep(2.8)

    time.sleep(300)
