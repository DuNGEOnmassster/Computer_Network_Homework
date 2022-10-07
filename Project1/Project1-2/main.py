from bitstring import Bits, BitArray
from time import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="CRC")

    parser.add_argument("-d","--dataset", default="./dataset/test.txt",
                        help="input file data for CRC")
    parser.add_argument("-b","--batch_size",default=16,
                        help="bit size of a pair of data to compare")

    return parser.parse_args()


class Sum_Register:
    def __init__(self, args):
        self.size = args.batch_size
        self.sum = [0 for i in range(self.size)]
        self.carry_in = 0

    def getAdd(self, list):
        for i in range(self.size -1, -1, -1):
            self.sum[i] += list[i] + self.carry_in
            if self.sum[i] > 1:
                self.sum[i] -= 2
                self.carry_in = 1
            else:
                self.carry_in = 0
        while self.carry_in == 1:
            for i in range(self.size -1, -1, -1):
                self.sum[i] += self.carry_in
                if self.sum[i] > 1:
                    self.sum[i] -= 2
                    self.carry_in = 1
                else:
                    self.carry_in = 0

    def getSum(self):
        Sum = []
        for i in range(self.size):
            if self.sum[i] == 0:
                Sum.append(1)
            else:
                Sum.append(0)
        return BitArray(Sum)


def read_file(file_path):
    with open(file_path, "rb") as f:
        row_data = Bits(f)
        bit_length = len(row_data)
        print("原始数据：", row_data)
        print("原始数据位数：", bit_length)
        # import pdb; pdb.set_trace()  
    return row_data, bit_length  


def printf(byte1, byte2, Sumr, flag):
    if flag:
        byte1.extend(byte2)
        data16 = byte1.copy()
        print("16位数据: ", data16)
        Sumr.getAdd(data16)
        print("当前和：", Sumr.sum)
        byte1.clear()
        byte2.clear()
    else:
        byte1.extend([0, 0, 0, 0, 0, 0, 0, 0])
        Sumr.getAdd(byte1)
        print("16位数据: ", byte1)
        print("当前和：", Sumr.sum)


def process():
    start_time = time()

    args = parse_args()
    Sumr = Sum_Register(args)
    row_data, bit_length = read_file(args.dataset)

    start = 0
    cnt = 1
    byte1 = []
    byte2 = []

    while start < bit_length:
        byte_temp = []
        for i in range(start, start + args.batch_size//2):
            byte_temp.append(row_data[i])
        if byte1 == []:
            byte1 = byte_temp.copy()
        elif byte2 == []:
            byte2 = byte_temp.copy()
        start = start + args.batch_size//2
        if byte1 != [] and byte2 != []:
            print(f"第{cnt}组:")
            printf(byte1, byte2, Sumr, flag=True)
            cnt = cnt + 1

    if byte1 != [] and byte2 == []:
        printf(byte1, byte2, Sumr, flag=False)
    
    end_time = time()
    print(f"耗时{end_time-start_time:2f} sec, 最终反码校验和:{Sumr.getSum()}")

if __name__ == "__main__":
    process()
