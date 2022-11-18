import base64
import struct

import argparse
from fcntl import ioctl
import socket

def mac_aton(a):
    return base64.b16decode(a.upper().replace(':', ''))


def fetch_iface_mac(iface, s=None):
    # create socket if given, any type is ok
    if not s:
        s = socket(socket.AF_INET, socket.SOCK_DGRAM)

    # pack iface name to struct ifreq
    iface_buf = struct.pack('64s', iface.encode('utf8'))

    # call ioctl to get hardware address
    # according to C header file, SIOCGIFHWADDR is 0x8927
    mac = ioctl(s.fileno(), 0x8927, iface_buf)[18:24]

    return mac


def send_ether(iface, to, _type, data, s=None):
    # if destination address is readable format, convert first
    if isinstance(to, str):
        to = mac_aton(to)

    # if data is str type, encode it first
    if isinstance(data, str):
        data = data.encode('utf8')

    # create raw socket if not given
    if s is None:
        s = socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    # bind to the sending iface
    s.bind((iface, 0))

    # get MAC address of sending iface, which is the source address
    fr = fetch_iface_mac(iface, s)

    with open("data/1111.avi", "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(1024)
            if not bytes_read:
                # file transmitting is done
                break
            # pack ethernet header
            header = struct.pack('!6s6sH', to, fr, _type)
            # pack ethernet frame
            frame = header + bytes_read

            # send the ethernet frame
            s.send(frame)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Send ethernet frame.')

    # Argument: name of iface for sending
    parser.add_argument('--iface', dest='iface', required=True)
    # Argument: destination MAC address
    parser.add_argument(
        '-t',
        '--to',
        dest='to',
        required=True,
    )
    # Argument: data to send
    parser.add_argument(
        '-d',
        '--data',
        dest='data',
        default='a' * 46,
        required=False,
    )
    # Argument: protocol type
    parser.add_argument(
        '-T',
        '--type',
        dest='_type',
        default='0x0900',
        required=False,
    )

    # parse arguments
    args = parser.parse_args()

    return args


def main():
    '''
        Entrance for the program.
    '''

    # parse command line arguments
    args = parse_arguments()

    # send ethernet frame according to given arguments
    send_ether(
        iface=args.iface,
        to=args.to,
        _type=eval(args._type),
        data=args.data,
    )

if __name__ == '__main__':
    main()

# python send_ether.py -i en0 -t b0:be:83:7a:20:fa -T 0x1024 -d "Hello, world"
# python send_ether.py -i enp7s0 -t 00:2B:67:6E:37:E3 -T 0x1024 -d "Hello, world"
