import threading
import argparse
from utils.utils import terminal

def parse_args():
    parser = argparse.ArgumentParser(description="Project3: connection bewteen 2 ternimals with CSMA/CD")

    parser.add_argument("--ColisionWindow", type=float, default=51.2e-6,
                        help="The duration of the collision window(2*\tau), default with 51.2μs in Ethernet")
    parser.add_argument("--Transmission_speed", default=10e6,
                        help="The data transmission speed in Ethernet, default with 10Mb/s")
    parser.add_argument("--max_retrans", type=int, default=16,
                        help="The Maximum number of retransmissions")
    parser.add_argument("--max_k", type=int, default=5,
                        help="The Maximum exponential range to defer retransmission times")
    parser.add_argument("--bus", type=list, default=[0],
                        help="Initialized bus for Thread")
    parser.add_argument("--frame_num", type=int, default=5,
                        help="The number of frames to be transmissed from upper network layer")

    return parser.parse_args()


def run(num, bus, args):
    computer = terminal(num, args)
    computer.send_message(bus)


def process():
    args = parse_args()
    # print(f"10e-6 = 10 * pow(10,6) = {10e-6} s")
    # print(f"2 * {args.ColisionWindow} * {args.Transmission_speed} = {get_minframe(args)}")
    t1 = threading.Thread(target=run, args=(1, args.bus, args))
    t2 = threading.Thread(target=run, args=(2, args.bus, args))
    t1.start()
    t2.start()

if __name__ == "__main__":
    process()