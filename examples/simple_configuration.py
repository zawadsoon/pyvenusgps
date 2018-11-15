#!/usr/bin/python3

import time
import serial
from functools import reduce
from pyvenusgps import VenusGPS

#create driver with baudrate wich is default
driver = serial.Serial(port='/dev/ttyS0', baudrate = 9600, timeout=1)

#Connect to gps and set higher baud rate
gps = VenusGPS(driver)
gps.querySoftwareVersion()
gps.configureSerialPort(VenusGPS.BAUD_RATE_115200)

#Disconnect from GPS
driver.close()

#Create new connection with higher baud rate and update driver in gps instance 
newDriver = serial.Serial(port='/dev/ttyS0', baudrate = 115200, timeout=1)
gps.setDriver(newDriver)

while 1:
    try:
        print(gps.read())
    except KeyboardInterrupt: 
        break

