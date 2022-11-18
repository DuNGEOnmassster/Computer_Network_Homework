from utils.utils import *
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Computer Network Project4")

    parser.add_argument("--sender_ip",default="127.0.0.1",
                        help="declare sender ip address")
    parser.add_argument("--receiver_ip", default='10.31.165.241',
                        help="declare recevier ip address")
    parser.add_argument("--min_data_size", type=int, default=1500,
                        help="declare minimum size of data")
    parser.add_argument("--max_data_size", type=int, default=5000,
                        help="declare maximum size of data")

    return parser.parse_args()


def process():
    args = parse_args()
    sender = Terminal(args.sender_ip, args)
    receiver = Terminal(args.receiver_ip, args)
    bus = []
    sender.create_ipGroup(args.receiver_ip)
    # sender.create_ipGroup('0.0.0.1')
    sender.send(bus)
    receiver.receive(bus)

if __name__ == "__main__":
    process()
