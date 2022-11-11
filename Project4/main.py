from utils.utils import *
import argparse
import ipaddress

def parse_args():
    parser = argparse.ArgumentParser(description="Computer Network Project4")

    parser.add_argument("--sender_ip",default="127.0.0.1",
                        help="sender ip address")
    parser.add_argument("--receiver_ip", default='10.31.2.4',
                        help="recevier ip address")

    return parser.parse_args()


def send():
    args = parse_args()
    sender = Terminal(args.sender_ip)
    receiver = Terminal(args.receiver_ip)
    bus = []
    receiver_ip2 = args.receiver_ip[:-1]+str(int(args.receiver_ip[-1])+64)
    sender.create_ipGroup(args.receiver_ip)
    sender.create_ipGroup(args.receiver_ip)
    # sender.create_ipGroup(receiver_ip2)
    sender.send(bus)
    receiver.receive(bus)


def try_ipv4():
    args = parse_args()
    ipaddr = ipaddress.IPv4Address(args.sender_ip)
    print(ipaddr)


if __name__ == "__main__":
    send()
    # try_ipv4()
