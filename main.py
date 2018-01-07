from settings import app_eui, app_key
from network import LoRa

import socket
import time
import pycom
import struct
import binascii

from pysense import Pysense
from lib.MPL3115A2 import MPL3115A2
from lib.LTR329ALS01 import LTR329ALS01
from lib.SI7006A20 import SI7006A20
from lib.LIS2HH12 import LIS2HH12

# Disable the heartbeat LED
pycom.heartbeat(False)

# Make the LED light up in black
pycom.rgbled(0x000000)

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, adr=True)

# Retrieve the dev_eui from the LoRa chip (Only needed for OTAA to retrieve once)
dev_eui = binascii.hexlify(lora.mac()).upper().decode('utf-8')

# Join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# Wait until the module has joined the network
count = 0
while not lora.has_joined():
    pycom.rgbled(0xffa500) # Make the LED light up in orange
    time.sleep(0.2)
    pycom.rgbled(0x000000) # Make the LED light up in black
    time.sleep(2)
    print("retry join count is:" ,  count)
    count = count + 1

print("join procedure succesfull")

# Show that LoRa OTAA has been succesfull by blinking blue
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
# Make the socket non-blocking
s.setblocking(False)

# Init the libraries
pysense = Pysense()
mpl3115a2 = MPL3115A2() # Barometric Pressure Sensor with Altimeter
ltr329als01 = LTR329ALS01() # Digital Ambient Light Sensor
si7006a20 = SI7006A20() # Humidity and Temperature sensor
lis2hh12 = LIS2HH12() # 3-Axis Accelerometer

while True:

    # Read the values from the sensors
    voltage = pysense.read_battery_voltage()
    temperature = mpl3115a2.temperature()
    pressure = mpl3115a2.pressure()
    light = ltr329als01.light()[0]
    humidity = si7006a20.humidity()
    roll = lis2hh12.roll()
    pitch = lis2hh12.pitch()

    # Debug sensor values
    print('voltage:{}, temperature:{}, pressure:{}, light:{}, humidity:{}, roll:{}, pitch:{}'.format(voltage, temperature, pressure, light, humidity, roll, pitch))

    clean_bytes = struct.pack(">iiiiiii",
        int(temperature * 100), # Temperature in celcius
        int(pressure * 100), # Atmospheric pressure in bar
        int(light * 100), # Light in lux
        int(humidity * 100), # Humidity in percentages
        int(roll * 100), # Roll in degrees in the range -180 to 180
        int(pitch * 100), # Pitch in degrees in the range -90 to 90
        int(voltage * 100)) # Battery voltage

    # send the data over LPWAN network
    s.send(clean_bytes)

    pycom.rgbled(0x007f00) # Make the LED light up in green
    time.sleep(0.2)
    pycom.rgbled(0x000000)
    time.sleep(2.8)

    # Wait for 60 seconds before moving to the next iteration
    time.sleep(60)
