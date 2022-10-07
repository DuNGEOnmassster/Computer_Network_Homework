from bitstring import Bits, BitArray
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="CRC")

    parser.add_argument("-d","--dataset", default="./dataset/test.txt",
                        help="input file data for CRC")
    parser.add_argument("-s","--segment_size",default=1500,
                        help="the max size of a single segment")
    parser.add_argument("-f","--fill_zero",default=True,
                        help="fill the lack with zero until smallest batch size")
    parser.add_argument("-l","--least_size",default=46,
                        help="the least size of a single segment")
    parser.add_argument("-b",default=32, type=int,
                        help="bits that CRC based on, and 32 is recommended")

    return parser.parse_args()


class CRC32:
    def __init__(self, data, args):
        self.data = data
        self.args = args
        self.gx = "100000100110000010001110110110111"
        self.r = args.b


    def encode(self):
        dividend = self.data + '0' * self.r
        dividend_len = len(dividend)
        temp = dividend[0: 32]
        add_bit = 32
        while add_bit < dividend_len:
            temp += dividend[add_bit]
            add_bit += 1
            if temp[0] == '1':
                for i in range(33):
                    if temp[i] == self.gx[i]:
                        temp = temp[:i]+'0'+temp[i+1:]
                    else:
                        temp = temp[:i]+'1'+temp[i+1:]
            temp = temp[1:]
        return self.data+temp # 原串要拼接32位寄存值


    def decode(self, code):
        dividend = code
        dividend_len = len(dividend)
        temp = dividend[0: 32]
        add_bit = 32
        while add_bit < dividend_len:
            temp += dividend[add_bit]
            add_bit += 1
            if temp[0] == '1':
                for i in range(33):
                    if temp[i] == self.gx[i]:
                        temp = temp[:i] + '0' + temp[i + 1:]
                    else:
                        temp = temp[:i] + '1' + temp[i + 1:]
            temp = temp[1:]
        if temp == '0' * 32:
            return True
        else:
            return False

def CRC_process(data, args):
    crc = CRC32(data, args)
    crc_code = crc.encode()
    crc_hex = BitArray('0b'+crc_code)
    print("crc编码: ", crc_hex)
    print("crc后32位: ", crc_hex[-32:])
    no_false = crc.decode(crc_code)
    if no_false:
        print("接收编码没有出错")
    else:
        print("接收编码出错")