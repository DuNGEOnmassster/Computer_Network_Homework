import socket
import numpy as np
from bitstring import BitArray

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
        self.options = opt_part             # 可选


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


    def get_head_len(self):
        if self.options is not None:
            le = 20+len(self.options//8)
        else:
            le = 20
        le = BitArray(bin(le//4))
        if len(le) < 4:
            le = BitArray(np.zeros(4-len(le))) + le
        self.head_len = le