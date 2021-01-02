import serial
import struct
import sys


class AT28C256(object):
    BUFFER_SIZE = 1536

    def __init__(self, port='COM4'):
        self.serial = serial.Serial(port, 115200)
        print('>>>>> AT28C256 Serial Connected ("', self.serial.readline().decode('ascii').strip(), '")', sep='')

    def read(self, address):
        self.serial.write(b'\x01' + struct.pack('<H', address & 0x7fff))
        return self.serial.read()

    def read_range(self, address, count):
        result = []

        for i in range(0, count, AT28C256.BUFFER_SIZE):
            chunk_size = count - i
            if chunk_size > AT28C256.BUFFER_SIZE:
                chunk_size = AT28C256.BUFFER_SIZE

            print('\r[+] AT28C256 Reading', ('%04x' % (address + i)), '-',  ('%04x' % (address + i + chunk_size)), '/', ('%04x' % (address + count)), end='')
            sys.stdout.flush()

            self.serial.write(b'\x02' + struct.pack('<HH', (address + i) & 0x7fff, chunk_size & 0x7fff))
            result.append(self.serial.read(size=chunk_size))

        print()
        return b''.join(result)

    def write(self, address, value):
        self.serial.write(b'\x03' + struct.pack('<HB', address & 0x7fff, value & 0xff))
        self.serial.read()

    def write_range(self, address, data):
        for i in range(0, len(data), AT28C256.BUFFER_SIZE):
            chunk_size = len(data) - i
            if chunk_size > AT28C256.BUFFER_SIZE:
                chunk_size = AT28C256.BUFFER_SIZE

            print('\r[+] AT28C256 Writing', ('%04x' % (address + i)), '-',  ('%04x' % (address + i + chunk_size)), '/', ('%04x' % (address + len(data))), end='')
            sys.stdout.flush()

            self.serial.write(b'\x04' + struct.pack('<HH', (address + i) & 0x7fff, chunk_size & 0x7fff) + data[i:i+chunk_size])
            self.serial.read()

        print()
