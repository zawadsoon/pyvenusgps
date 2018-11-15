#!/usr/bin/python3

import time
import serial
from functools import reduce
from pyvenusgps import VenusGPS

driver = serial.Serial(port='/dev/ttyS0', baudrate = 9600, timeout=1)

gps = VenusGPS(driver)

gps.querySoftwareVersion()
gps.configureSerialPort(VenusGPS.BAUD_RATE_9600)

while 1:
    try:
        print(gps.read())
    except KeyboardInterrupt: 
        break

