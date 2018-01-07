# TTN Flevoland - Pysense Workshop

## The Things Network

### Make sure to have your account registered at The Things Network
Registering you account can be done at
https://account.thethingsnetwork.org/register

If you want to chat with us request for a Slack account by pressing the [request Slack invite] link.

Make sure that your username is connected to 'ttn-flevoland-pysense' application.
https://console.thethingsnetwork.org/applications/ttn-flevoland-pysense

### Application EUI
- AppEUI: This is a unique application identifier used to group objects. This address, 64 bits, is used to classify the peripheral devices by application. This setting can be adjusted.

The Application EUI is an End Device Unique Identifier generated while creating this application. The EUI 70B3D57ED0008AC8 will be used later on in our configuration.

### The known devices registered for this application can be found here
https://console.thethingsnetwork.org/applications/ttn-flevoland-pysense/devices

### New devices
A new device can be added here.
https://console.thethingsnetwork.org/applications/ttn-flevoland-pysense/devices/register

- DeviceID : A unique name
- DeviceEUI : This identifier, factory set, makes each object unique. In principle, this setting cannot be adjusted., The MAC address of the LoRa chipset
- AppKey: This is a secret key shared between the peripheral device and the network. It is used to determine the session keys. This setting can be adjusted. For this workshop the key 'FA91AF8E029ABB8E45B131FE0392F3AA' is added for all devices.

#### Frame counters
It is however possible to re-transmit the messages. These so-called replay attacks can be detected and blocked using frame counters.

When a device is activated, these frame counters (FCntUp and FCntDown) are both set to 0. Every time the device transmits an uplink message, the FCntUp is incremented and every time the network sends a downlink message, the FCntDown is incremented. If either the device or the network receives a message with a frame counter that is lower than the last one, the message is ignored.

This security measure has consequences for development devices, which often are statically activated (ABP). When you do this, you should realize that these frame counters reset to 0 every time the device restarts (when you flash the firmware or when you unplug it). As a result, The Things Network will block all messages from the device until the FCntUp becomes higher than the previous FCntUp. Therefore, you should re-register your device in the backend every time you reset it.

For development devices the setting [Frame Counter Checks] is unchecked.

#### Activation types
There are two ways of activating a device on the network. OTAA is more secure and default.

OTAA: Over-The-Air-Activation
Over-the-Air Activation (OTAA) is the preferred and most secure way to connect with The Things Network. Devices perform a join-procedure with the network, during which a dynamic DevAddr is assigned and security keys are negotiated with the device.

ABP: Activation By Personalization
Activation by Personalization (ABP)
In some cases you might need to hardcode the DevAddr as well as the security keys in the device. This means activating a device by personalisation (ABP). This strategy might seem simpler, because you skip the join procedure, but it has some downsides related to security.

## Pycom
https://www.gitbook.com/book/pycom/pycom-documentation/details

### Boot modes
An error occurred: Not enough memory available on the board.
Upload failed. Please reboot your device manually.

import os

### Flash firmware
If you need to update the firmware go to:
https://docs.pycom.io/chapter/pytrackpysense/installation/firmware.html and install the latest version.
Currently installed 0.0.8 firmware


## Connecting your device

### Install and configure the preferred IDE
Go to https://atom.io and download the IDE.

### Install plugins
Go to Settings and +Install
Search for the packages
- autocomplete-python
- pymakr

### Create an empty project
Make sure you have created a project directory on your local machine, eg.: /home/user/projects/pycom-pysense
In Atom add this directory by: File -> Add Project Folder

### Configure Pymakr
change ip to: tty
More: get serial ports - > copied to clipoard
Sync folder: .






## Retrieve the MAC address of the LoRa chip
## Retrieve dev_eui
### Retrieve the dev_eui from the LoRa chip (Only needed for OTAA to retrieve once)
dev_eui = binascii.hexlify(lora.mac()).upper().decode('utf-8')
print(dev_eui)



## Messages in Binary
Don’t waste your time!

Simple:
{ “Count”: 1234, "Temperature": 20.635 }
40 bytes: 292 messages per day (SF7)
Remove counter (is already included in header), spaces, and compress names:
{“t”:20.63}
11 bytes: 486 messages per day
No JSON:
20.63
5 bytes: 582 messages per day
Signed 16 bit integer
0x080F
2 bytes: 648 messages per day




## API
https://ttn-flevoland-pysense.data.thethingsnetwork.org






## Links

https://www.thethingsnetwork.org/forum/t/what-is-the-difference-between-otaa-and-abp-devices/2723
https://www.thethingsnetwork.org/docs/devices/bytes.html


https://docs.python.org/2/library/struct.html




https://blog.dbrgn.ch/2017/6/23/lorawan-data-rates/

https://zakelijkforum.kpn.com/lora-forum-16/over-the-air-activation-otaa-8323


https://www.jaguar-network.com/en/news/lorawan-in-a-nutshell-2-internet-of-things-iot/
https://docs.pycom.io/chapter/pytrackpysense/apireference/pysense.html
https://startiot.telenor.com/learning/pysense-quick-start-guide/
https://forum.pycom.io/topic/2001/pysense-accuracy
