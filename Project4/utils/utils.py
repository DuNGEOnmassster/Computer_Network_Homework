from socket import socket
# 开发时间 2022/11/4 22:26
import random
import numpy as np
from bitstring import BitArray
from utils import common


class IpHead:
    def __init__(self, version, service, id_ip, sign, slice_shift, time_to_live, protocol, srcAddr, dstAddr, opt_part=None):
        self.version = version              # ip版本，4bit
        self.head_len = None                # 首部长度，4bit
        self.service = service              # 服务类型，8bit
        self.total_len = None               # ip分组总长度。16bit
        self.id = id_ip                     # 标识，16bit
        self.sign = sign                    # 分片标志，3bit
        self.slice_shift = slice_shift      # 片偏移，13bit
        self.ttl = time_to_live             # 生存时间，8bit
        self.protocol = protocol            # 协议，8bit
        self.HdrChsum = None                # 简单校验和，16位
        self.srcAddr = srcAddr              # 源地址，32bit
        self.dstAddr = dstAddr              # 目的地址，32it
        self.options = opt_part

    # 计算首部大小
    def get_head_len(self):
        if self.options is not None:
            le = 20+len(self.options//8)
        else:
            le = 20
        le = BitArray(bin(le//4))
        if len(le) < 4:
            le = BitArray(np.zeros(4-len(le))) + le
        self.head_len = le

    # 计算总长度
    def get_total_len(self, data):
        head_len_int = 0
        for i in range(4):
            head_len_int += 2**(3-i) * self.head_len[i]
        head_len_int = int(head_len_int*4) # 单位:字节
        total_len_int = int(head_len_int + len(data)//8)
        total_len_bit = BitArray(bin(total_len_int))
        if len(total_len_bit) < 16:
            total_len_bit = BitArray(np.zeros(16-len(total_len_bit))) + total_len_bit
        self.total_len = total_len_bit

    # 计算校验和
    def get_HdrChsum(self):
        bitarray = self.version+self.head_len+self.service+self.total_len+self.id+self.sign+self.slice_shift+self.ttl+self.protocol+self.srcAddr+self.dstAddr+self.options
        container = common.sum_container()
        for i in range(0, len(bitarray), 16):
            container.add(bitarray[i:i+16])
        solution = container.getSumSolution()
        self.HdrChsum = solution

    # 合成bit流
    def get_bits(self):
        bits = BitArray([])
        bits += self.version # ip版本，4bit
        bits += self.head_len  # 首部长度，4bit
        bits += self.service  # 服务类型，8bit
        bits += self.total_len  # ip分组总长度。16bit
        bits += self.id # 标识，16bit
        bits += self.sign  # 分片标志，3bit
        bits += self.slice_shift  # 片偏移，13bit
        bits += self.ttl  # 生存时间，8bit
        bits += self.protocol  # 协议，8bit
        bits += self.HdrChsum  # 简单校验和，16位
        bits += self.srcAddr  # 源地址，32bit
        bits += self.dstAddr  # 目的地址，32it
        bits += self.options
        return bits


class IpGroup:
    def __init__(self, head:IpHead, data):
        self.Header = head
        self.data = data


class Terminal:
    def __init__(self, ip):
        self.ip_str = ip
        self.ip = self.translate_ip(ip)
        self.identification = 0    # 创建ip分组的标识
        self.slice_joint = []      # 分片处理队列
        self.send_queue = []       # 发送队列
        self.recv_queue = []       # 接收队列

    # 将IP地址转化成二进制
    def translate_ip(self, ip: str):
        ip_parts = ip.split('.')
        ip = BitArray([])
        for part in ip_parts:
            part = bin(int(part))
            part = BitArray(part)
            if len(part) < 8:
                part = BitArray(np.zeros(8-len(part))) + part
                ip += part
        return ip

    def create_data(self):
        seed = random.randint(0, 5000)*8 # 随机数据大小
        data_list = np.random.randint(0, 2, seed)
        data_bitarray = BitArray(data_list)
        return data_bitarray

    def create_service(self):
        priority = np.random.randint(0, 2, 3)
        DTRC = np.random.randint(0, 2, 4)
        li = np.append(priority, DTRC)
        zero = np.zeros(1, dtype=int)
        li = np.append(li, zero)
        return BitArray(li)

    def create_id(self):
        id_ip = bin(self.identification)
        id_ip = BitArray(id_ip)
        if len(id_ip) < 16:
            id_ip = BitArray(np.zeros(16-len(id_ip))) + id_ip
        return id_ip

    # 准备首部各部分
    def create_ipHeader(self, destination):
        version = BitArray([0, 1, 0, 0])    # ipv4
        service = self.create_service()
        id_ip = self.create_id()
        sign = BitArray([0, 0, 0])
        slice_shift = BitArray(np.random.randint(0, 1, 12))
        # 分片设置初始化，需要根据数据决定如何填写
        time_to_live = BitArray([0, 1, 0, 0, 0, 0, 0, 0])  # 生存时间初始化为64
        protocol = BitArray([0, 0, 0, 0, 0, 0, 0, 0])   # 上层的协议编号，此处全零替代
        srcAddr = self.ip
        dstAddr = self.translate_ip(destination)

        head = IpHead(version, service, id_ip, sign, slice_shift, time_to_live, protocol, srcAddr, dstAddr)
        return head

    def create_ipGroup(self, dst):
        groups = []
        data = self.create_data()
        data_len = len(data)
        start = 0
        while True:
            head = self.create_ipHeader(dst)
            data_slice = data[start:start+12000-160]
            # 获取片偏移
            slice_shift = BitArray(bin(start//8//8))
            if len(slice_shift) < 13:
                slice_shift = BitArray(np.zeros(13 - len(slice_shift))) + slice_shift
            head.slice_shift = slice_shift
            # 判断是最终分片与否来设置标志
            if start+12000-160 >= data_len:
                head.sign = BitArray([0, 0, 0])
                head.get_head_len()
                head.get_total_len(data_slice)
                head.get_HdrChsum()
                group = IpGroup(head, data_slice)
                groups.append(group)
                self.identification += 1
                break
            else:
                head.sign = BitArray([0, 0, 1])
                head.get_head_len()
                head.get_total_len(data_slice)
                head.get_HdrChsum()
                group = IpGroup(head, data_slice)
                groups.append(group)
                start += 12000-160
        for group in groups:
            self.send_queue.append(group)

    def translate_version(self, group):
        bits = group[0:4]
        num = common.binary_to_int(bits, 4)
        print(f"[INFO]----> Version: IPv{num}")
        return num

    def translate_head_len(self, group):
        head_len_bin = group[4:8]
        head_len_int = common.binary_to_int(head_len_bin, 4)*4
        print(f"[INFO]----> IP首部长度: {head_len_int} Bytes")
        return head_len_int

    def translate_service(self, group):
        service = group[8:16]
        priority = service[0:3]
        priority_int = common.binary_to_int(priority, 3)
        D = service[3]
        T = service[4]
        R = service[5]
        C = service[6]
        print(f"[INFO]----> Service: priority {priority_int}, 低延迟：{D}, 高吞吐量：{T}, 高可靠性：{R}, 选择代价更小链路：{C}")
        return priority_int, D, T, R, C

    def translate_total_len(self, group):
        total_len_bin = group[16:32]
        total_len_int = common.binary_to_int(total_len_bin, 16)
        print(f"[INFO]----> IP分组总长度：{total_len_int} Bytes")
        return total_len_int

    def translate_id(self, group):
        id_ip = group[32:48]
        id_ip = common.binary_to_int(id_ip, 16)
        print(f"[INFO]----> 该分组ID：{id_ip}")
        return id_ip

    def translate_slice(self, group):
        flag = group[48:51]
        shift = group[51:64]
        shift_int = common.binary_to_int(shift, 13)
        print("[INFO]----> 开始解析分片相关参数...")
        if flag[1]:
            print("  DF:该分组不允许再分片")
        else:
            print("  DF:该分组允许再分片")
        if flag[2]:
            print("  MF:这是一个分片且后续还有分片")
        else:
            print("  MF:最终分片或单独分组")
        print(f"  Shift:{shift_int}*8 Byte")
        return flag[2], shift_int

    def translate_ttl(self, group):
        ttl_bin = group[64:72]
        ttl_int = common.binary_to_int(ttl_bin, 8)
        print(f"[INFO]----> 分组剩余生命周期：{ttl_int}")
        return ttl_int

    def translate_protocol(self, group):
        prot = group[72:80]
        prot_int = common.binary_to_int(prot, 8)
        print(f"[INFO]----> 使用协议：{prot_int}号")
        return prot_int

    def translate_Addr(self, group):
        src = group[96:128]
        dst = group[128:160]
        src = common.binAddr_to_ip(src)
        dst = common.binAddr_to_ip(dst)
        print(f"[INFO]----> 源地址：{src}，目的地址：{dst}")
        return src, dst

    def translate(self, group):
        print("A group translation begins...")
        src, dst = self.translate_Addr(group)
        if dst != self.ip_str:
            print("[Exception]--> Unmatched IP group!")
        else:
            version = self.translate_version(group)
            head_len = self.translate_head_len(group)
            priority, d, t, r, c = self.translate_service(group)
            total_len = self.translate_total_len(group)
            id_ip = self.translate_id(group)
            flag, shift = self.translate_slice(group)
            ttl = self.translate_ttl(group)
            protocol = self.translate_protocol(group)
            if flag or (shift != 0):
                i = 0
                while i < len(self.slice_joint):
                    if self.slice_joint[i][2] > shift:
                        break
                    i += 1
                self.slice_joint.insert(i, [id_ip, flag, shift, group[head_len*8:]])
        print()

    def send(self, bus):
        while len(self.send_queue) != 0:
            a_group = self.send_queue.pop(0)
            group_bits = a_group.Header.get_bits()
            group_bits += a_group.data
            bus.append(group_bits)

    def receive(self, bus):
        while len(bus) !=0:
            self.recv_queue.append(bus.pop(0))
        for group in self.recv_queue:
            self.translate(group)
        # get rid of slices...
        while len(self.slice_joint) != 0:
            base = self.slice_joint.pop(0)
            length = len(self.slice_joint)
            i = 0
            while i < length:
                if base[0] == self.slice_joint[i][0]:
                    base[3] += self.slice_joint[i][3]
                    self.slice_joint.pop(i)
                    length -= 1
            print(f"Got a connected group{base[0]},len_data: {len(base[3])//8} Bytes, data: {base[3]}")
