# TTN Flevoland - Pysense Workshop


## Boot modes
https://docs.pycom.io/chapter/toolsandfeatures/bootmodes.html

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



## Links
https://docs.pycom.io/chapter/pytrackpysense/apireference/pysense.html
https://startiot.telenor.com/learning/pysense-quick-start-guide/
https://forum.pycom.io/topic/2001/pysense-accuracy
