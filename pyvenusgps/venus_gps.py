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

    
