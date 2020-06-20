import serial
import struct


class AT28C256(object):

    def __init__(self, port='COM4'):
        self.serial = serial.Serial(port, 115200)
        print('>>>>> AT28C256 Serial Connected ("', self.serial.readline().decode('ascii').strip(), '")', sep='')

    def read(self, address):
        self.serial.write(b'\x01' + struct.pack('<H', address & 0x7fff))
        return self.serial.read()

    def read_range(self, address, count):
        v = b''
        for i in range(0, count):
            v += self.read(address + i)
        return v

    def write(self, address, value):
        self.serial.write(b'\x02' + struct.pack('<HB', address & 0x7fff, value & 0xff))
        return self.serial.read()

    def write_range(self, address, data):
        for i in range(0, len(data)):
            self.write(address + i, data[i])
