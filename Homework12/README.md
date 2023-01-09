# Homework for the 12th

#### 作业


作业1 ： 某单位有5个物理网络，申请一个C类网段IP地址块 （200.200.200.0/24），物理网段主机数量为：60、60、60、30、30。如果你是该单位网络管理员，请写出你划分子网的方案。

（1）你在划分子网时，采用定长子网掩码还是变长子网掩码？

（2）请分析出划分的每一个子网的网络地址、直接广播地址、可分配的IP地址以及该子网的网络地址
        
分析如下

使用2比特位作为子网号，可划分4个子网，每个子网64-2台主机；如果采用3比特位作为子网号，可划分8个子网，每个子网32-2台主机；

解决方法：

（1）先采用2比特子网号，从4个子网中取一个子网再采用1比特划分为两个子网。

（2）先采用26个连续1子网掩码（255.255.255.192）将网络划分为4个子网（每个62台主机）

（3）采用27个连续1子网掩码（ 255.255.255.224 ）将4个子网之一划分为2个小规模网络（每个小子网最多30台主机）


作业2  校园网在进行IP地址分配时，给某基层单位分配了一个C类地址块202.117.110.0/24，该单位的计算机数量分布如表1-1所示。要求各部门处于不同的网段，请填写表1-2中的（3）～（10）处空缺的主机地址（或范围）和子网掩码。（12分）







作业3：一个单位申请到四个C类地址快，202.197.8.0/24, 202.197.9.0/24, 202.197.10.0/24, 202.197.11.0/24，如果你是管理员，需要构建一个超网，请写出该超网的网络地址、直接广播地址、可分配的IP地址以及超网掩码。


分析如下：
|   |   202.197.8.0/24 ： 202.117.00001000.00000000 |
|   |   202.197.9.0/24 ： 202.117.00001001.00000000 |
|   |   202.197.10.0/24： 202.117.00001010.00000000 |
|   |   202.197.11.0/24： 202.117.00001011.00000000 |

See [Mingzhe's implementation](https://github.com/DuNGEOnmassster/Computer_Network_Homework/tree/mingzhe/Homework12) and [Zhengbao's implementation](https://github.com/DuNGEOnmassster/Computer_Network_Homework/tree/zhengbao/Homework12)