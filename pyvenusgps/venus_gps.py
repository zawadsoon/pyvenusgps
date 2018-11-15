#!/usr/bin/python3

import serial
from functools import reduce

class VenusGPS:
    BAUD_RATE_4800 = 0x00
    BAUD_RATE_9600 = 0x01
    BAUD_RATE_19200 = 0x02
    BAUD_RATE_38400 = 0x03
    BAUD_RATE_57600 = 0x04
    BAUD_RATE_115200 = 0x05

    ATTRIBUTES_UPDATE_TO_SRAM = 0x00
    ATTRIBUTES_UPDATE_TO_SRAM_AND_FLASH = 0x01
    ATTRIBUTES_TEMPORARILY_ENABLED = 0X02

    MESSAGE_TYPE_NO_OUTPUT = 0x00
    MESSAGE_TYPE_NMEA = 0x01
    MESSAGE_TYPE_BINARY = 0x02

    POWER_MODE_NORMAL = 0X00
    POWER_MODE_POWER_SAVE = 0X01

    def __init__(self, driver):
        self.setDriver(driver)

    def read(self):
        return self.driver.readline()

    def write(self, mbytes):
        return self.driver.write(mbytes)

    def setDriver(self, driver):
        self.driver = driver

    def checkSum (self, data):
        return [reduce(lambda x, y: x ^ y, data)]

    def cmdToString(self, cmd):
        return '[ ' + ''.join(format(x, '02x') + ' ' for x in cmd) + ']'
    
    def dataLength (self, data):
        b1, b2, b3, b4 = (len(data) & 0xFFFFFFFF).to_bytes(4, 'big')
        return [b3, b4]

    def getFrame(self, data):
       return bytes([0xA0, 0xA1] + self.dataLength(data) + data + self.checkSum(data) + [0x0D, 0x0A])

    def querySoftwareVersion(self):
        self.driver.write(self.getFrame([0x02, 0x00]))
        self.driver.flush()

    def configureSerialPort(self, baud_rate, attributes = ATTRIBUTES_UPDATE_TO_SRAM):
        self.driver.write(self.getFrame([0x05, 0x00, baud_rate, attributes]))
        self.driver.flush()

    def configureNMEAMessage(self, GGAInterval = 0x01, GSAInterval = 0x01, GSVInterval = 0x01, GLLInterval = 0x01, RMCInterval = 0x01, VTGInterval = 0x01, VTHInterval = 0x01, ZDAInterval = 0x01, attributes = ATTRIBUTES_UPDATE_TO_SRAM): 
        self.driver.write(self.getFrame([0x08, 0x00, GGAInterval, GSAInterval, GSVInterval, GLLInterval, RMCInterval, VTGInterval, VTHInterval, ZDAInterval, attributes])) 
        self.driver.flush() 

    def configureMessageType(self, message_type = MESSAGE_TYPE_NMEA):
        self.driver.write(self.getFrame([0x09, message_type]))
        self.driver.flush()

    def configureSystemPowerMode(self, mode, attributes = ATTRIBUTES_UPDATE_TO_SRAM):
        self.driver.write(self.getFrame([0x0c, mode, attributes]))
        self.driver.flush()

    
