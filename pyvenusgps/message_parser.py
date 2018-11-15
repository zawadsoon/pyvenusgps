#!/usr/bin/python3

import serial
from functools import reduce

def i (m):
    return str(int(m))

class MessageParser:
    def __init__(self, ignore_ack = False):
        self.ignore_ack = ignore_ack 

    def parse(self, sbytes):
        if len(sbytes) < 4: 
            return sbytes

        message_id = sbytes[4]

        if message_id in [0x80, 0x81, 0x83, 0x84, 0x86, 0xb5]: 
            return self.resolveParser(
                    message_id,
                    self.getMessageBody(sbytes)
                )

        return sbytes

    def getMessageBody(self, sbytes):
        return sbytes[3: len(sbytes) - 3]

    def resolveParser(self, message_id, message_body):
        #This is empty value just for easier match docs, now byte with index 4 match byte 4 in docs
        message_body = bytearray(0x00) + message_body
        if message_id is 0x80:
            return self.parseSoftwareVersion(message_body)
        elif message_id is 0x81:
            return self.parseSoftwareCRC(message_body)
        elif message_id is 0x83:
            if self.ignore_ack: return None
            else: return self.parseACK(message_body)
        elif message_id is 0x84:
            if self.ignore_ack: return None
            else: return self.parseNACK(message_body)
        elif message_id is 0x86:
            return self.parsePositionUpdateRate(message_body)
        elif message_id is 0xb5:
            return self.parseGPSNavigationMode(message_body)

    def getSoftwareType(self, mb):
        software_type = None
        if mb[2] is 0x00: software_type = 'Reserved'
        elif mb[2] is 0x01: software_type = 'System code'
        return 'Software type: ' + software_type + '\n'

    def parseSoftwareVersion(self, mb):
        msg =  'Software Version\n' 
        msg += self.getSoftwareType(mb)
        msg += 'Kernel Version: ' + i(mb[3]) + '.' + i(mb[4]) + '.' + i(mb[5]) + '.' + i(mb[6]) + '\n'
        msg += 'ODM version: ' + i(mb[7]) + '.' + i(mb[8]) + '.' + i(mb[9]) + '.' + i(mb[10]) + '\n'
        msg += 'Revision: ' + i(mb[11]) + i(mb[12]) + i(mb[13]) + i(mb[14])
        return msg

    def parseSoftwareCRC(self, mb):
        software_type = None
        if mb[2] is 0x00: software_type = 'Reserved'
        elif mb[2] is 0x01: software_type = 'System code'
        
        msg =  'Software CRC\n' 
        msg += self.getSoftwareType(mb)
        msg += 'CRC: ' + i(mb[3]) + i(mb[4])
        return msg

    def parseACK(self, mb):
        return 'ACK | Message ID: ' + hex(mb[1]) + ', ACK ID: ' + hex(mb[2])

    def parseNACK(self, mb):
        return 'NACK | Message ID: ' + hex(mb[1]) + ', ACK ID: ' + hex(mb[2])

    def parsePositionUpdateRate(self, mb):
        return 'Position update rate: ' + i(mb[2])

    def parseGPSNavigationMode(self, mb):
        navigation_mode = None

        if mb[2] is 0x00: navigation_mode = 'car'
        elif mb[2] is 0x01: navigation_mode = 'pedestrian'

        return 'GPS navigation mode: ' + navigation_mode


