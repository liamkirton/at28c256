def hexdump(b, address=0):
    for i in range(0, len(b), 16):
        b_slice = b[i:i+16]
        b_slice = b_slice + bytes(16 - len(b_slice))
        b_hex = ' '.join([f'{v:02x}' for v in b_slice])
        b_chr = ''.join(['%c' % (v if v >= 0x20 and v < 0x7f else '.') for v in b_slice])
        print(f'[{address+i:04x}]  ', b_hex, '  ', b_chr)
