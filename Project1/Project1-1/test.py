import zlib
from bitstring import Bits

data = "0101010101010101010101111"
bdata = bytes(data, encoding="utf-8")
crc = zlib.crc32(bdata)
print(crc)
