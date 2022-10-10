from bitstring import Bits, BitArray
import argparse
from time import time


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
    parser.add_argument("-b","--batch_size",default=32, type=int,
                        help="bits that CRC based on, and 32 is recommended")
    parser.add_argument("-g","--ground",default="100000100110000010001110110110111",
                        help="ground that given by problem description")

    return parser.parse_args()


class CRC32:
    def __init__(self, data, args):
        self.data = data
        self.args = args
        self.g = args.ground
        self.r = args.batch_size

    def encode(self):
        dividend = self.data + '0' * self.r
        dividend_len = len(dividend)
        temp = dividend[0: self.r]
        add_bit = self.r
        while add_bit < dividend_len:
            temp += dividend[add_bit]
            add_bit += 1
            if temp[0] == '1':
                for i in range(self.r+1):
                    if temp[i] == self.g[i]:
                        temp = temp[:i]+'0'+temp[i+1:]
                    else:
                        temp = temp[:i]+'1'+temp[i+1:]
            temp = temp[1:]
        return self.data+temp

    def decode(self, code):
        dividend = code
        dividend_len = len(dividend)
        temp = dividend[0: self.r]
        add_bit = self.r
        while add_bit < dividend_len:
            temp += dividend[add_bit]
            add_bit += 1
            if temp[0] == '1':
                for i in range(self.r+1):
                    if temp[i] == self.g[i]:
                        temp = temp[:i] + '0' + temp[i + 1:]
                    else:
                        temp = temp[:i] + '1' + temp[i + 1:]
            temp = temp[1:]
        if temp == '0' * 32:
            return True
        else:
            return False


def load_file(file_path):
    with open(file_path, "rb") as f:
        row_data = Bits(f)
        bit_length = len(row_data)
        print("原始数据:", row_data)
        print("原始数据位数:", bit_length)
        # import pdb; pdb.set_trace()  
    return row_data, bit_length 


def get_segment(args):
    row_data, bit_length = load_file(args.dataset)
    start = 0
    segment_data = [] # list to store segments
    while start <= bit_length:
        segment_data.append(row_data[start:start+args.segment_size]) if start + args.segment_size - 1 < bit_length else segment_data.append(row_data[start:bit_length])
        start = start + args.segment_size
    for data in segment_data:
        print("数据段: ", data)
        data_str = ''
        for bit in data:
            data_str += '1' if bit else '0'
        print("字符串化:", data_str)
        if len(data) < args.least_size:
            data_str += '0' * (args.least_size - len(data))
            print(f"补零{len(data_str)}位")
    return data_str


def CRC_process(data, args):
    CRC_model = CRC32(data, args)
    CRC_hex = BitArray('0b'+CRC_model.encode())
    print("CRC编码: ", CRC_hex)
    print("CRC后32位: ", CRC_hex[-32:])
    if CRC_model.decode(CRC_model.encode()):
        print("接收编码无误")
    else:
        print("接收编码有误")


def process():
    start_time = time()
    args = parse_args()
    segment = get_segment(args)
    CRC_process(segment, args)
    end_time = time()
    print(f"耗时{end_time-start_time:2f} sec")
    

if __name__ == "__main__":
    process()
