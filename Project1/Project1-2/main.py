from bitstring import Bits
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="CRC")

    parser.add_argument("-d","--dataset", default="./dataset/test.txt",
                        help="input file data for CRC")
    parser.add_argument("-b","--batch_size",default=16,
                        help="bit size of a pair of data to compare")

    return parser.parse_args()

if __name__ == "__main__":
    pass
