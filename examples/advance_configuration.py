#!/usr/bin/python3

import time
import serial
from functools import reduce
from pyvenusgps import VenusGPS, MessageParser

msgp = MessageParser()

driver = serial.Serial(port='/dev/ttyS0', baudrate = 115200, timeout=1)

gps = VenusGPS(driver)
gps.setDriver(driver)

gps.querySoftwareVersion()
gps.queryPositionUpdateRate()
gps.queryNavigationMode()


while 1:
    try:
        msg = msgp.parse(gps.read())
        print(msg)
    except KeyboardInterrupt: 
        gps.close()
        break

