#!/usr/bin/python3

import time
import serial
from functools import reduce
from pyvenusgps import VenusGPS

#create driver with baudrate wich is default
driver = serial.Serial(port='/dev/ttyS0', baudrate = 115200, timeout=1)

#Connect to gps and set higher baud rate
gps = VenusGPS(driver)

gps.setDriver(driver)
gps.querySoftwareVersion()
gps.configureNMEAMessage(GGAInterval = 0x01, GSAInterval = 0x00, GSVInterval = 0x00, GLLInterval = 0x00, RMCInterval = 0x00, VTGInterval = 0x00, VTHInterval = 0x00, ZDAInterval = 0x00,)
gps.configureMessageType(VenusGPS.MESSAGE_TYPE_NMEA)
gps.configureSystemPositionRate(VenusGPS.RATE_20_HZ)
gps.queryPositionUpdateRate()
gps.queryDatum()
gps.configureNaviagtionMode(VenusGPS.NAVIGATION_MODE_PEDESTRIAN)
gps.queryNavigationMode()

while 1:
    try:
        msg = gps.read()
        print(msg)
    except KeyboardInterrupt: 
        gps.close()
        break

