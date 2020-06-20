import argparse

import at28c256


def run(port):
    a = at28c256.AT28C256(port=port)

    for i in range(0, 0x8000, 0x100):
        a.write_range(i, bytes(0x100))
        at28c256.hexdump(a.read_range(i, 0x100), address=i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=str)
    args = parser.parse_args()

    if not args.port:
        raise Exception('Invalid COM PORT')

    run(args.port)
