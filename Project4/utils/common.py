# 开发时间 2022/11/4 23:05
from bitstring import BitArray


class sum_container:
    def __init__(self):
        self.sum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.carry_in = 0

    def add(self, list):
        for i in range(15, -1, -1):
            self.sum[i] += list[i] + self.carry_in
            if self.sum[i] > 1:
                self.sum[i] -= 2
                self.carry_in = 1
            else:
                self.carry_in = 0
        while self.carry_in == 1:
            for i in range(15, -1, -1):
                self.sum[i] += self.carry_in
                if self.sum[i] > 1:
                    self.sum[i] -= 2
                    self.carry_in = 1
                else:
                    self.carry_in = 0

    def getSumSolution(self):
        solution = []
        for i in range(16):
            if self.sum[i] == 0:
                solution.append(1)
            else:
                solution.append(0)
        solution = BitArray(solution)
        return solution


def binary_to_int(bits:BitArray, length):
    sum_int = 0
    for i in range(length):
        sum_int += 2**(length-i-1) * bits[i]
    return sum_int


def binAddr_to_ip(bits:BitArray):
    ans = ''
    for i in range(0, 32, 8):
        section = binary_to_int(bits[i:i+8], 8)
        ans += str(section)
        if i != 24:
            ans += '.'
    return ans