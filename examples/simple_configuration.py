#!/usr/bin/python3

import time
import serial
from functools import reduce
from pyvenusgps import VenusGPS, MessageParser

#Create parser object
mgsp = MessageParser(ignore_ack = True)

#create driver with baudrate wich is default
driver = serial.Serial(port='/dev/ttyS0', baudrate = 9600, timeout=1)

#Connect to gps and set higher baud rate
gps = VenusGPS(driver)
gps.configureSerialPort(VenusGPS.BAUD_RATE_115200)

#Disconnect from GPS
driver.close()

#Create new connection with higher baud rate and update driver in gps instance 
newDriver = serial.Serial(port='/dev/ttyS0', baudrate = 115200, timeout=1)

#Set driver and flush
gps.setDriver(newDriver)
gps.read()

#Query software version
gps.querySoftwareVersion()

#Sets only GAA NMEA messages
gps.configureNMEAMessage(GGAInterval = 0x01, GSAInterval = 0x00, GSVInterval = 0x00, GLLInterval = 0x00, RMCInterval = 0x00, VTGInterval = 0x00, VTHInterval = 0x00, ZDAInterval = 0x00,)

#Set NMEA message type
gps.configureMessageType(VenusGPS.MESSAGE_TYPE_NMEA)

#Set refresh rate to 20Hz
gps.configureSystemPositionRate(VenusGPS.RATE_20_HZ)
gps.queryPositionUpdateRate()

while 1:
    try:
        msg = mgsp.parse(gps.read())
        if msg is not None:
            print(msg)
    except KeyboardInterrupt: 
        gps.close()
        break

