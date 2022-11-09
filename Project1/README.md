# Project for the 1st

# Project  1-1：计算CRC冗余校验码（32）
#### （1）给定一个文件，文件中的数据作为计算对象，如果文件数据不足46比特，利用若干0填充到46比特；如果文件数据大于1500字节，则分段计算各自的CRC校验码,每个数据段最大1500字节。 
#### （2）

![](./description2.png)

#### 结果：
##### DOS> 可执行文件名(Checksum-crc32)   数据文件
##### DOS>1 frame crc-32: ********;  2 frame crc-32: ********;
#####              …….          (用16进制显示) 


# Project   1-2：简单校验和（32）
### （1）给定一个文件，文件中的数据作为计算对象；
### （2）16比特位对齐相加；将高16比特位的进位再加；计算机结果取反作为简单校验和；
#### 要求：（1）每次只能从文件读取1个字节，先读取的字节为高8位，后读取的字节为低8位；（2）如果数据文件字节数奇数倍，则需要补一个字节（0X00）.
#### 结果：dos>check sum  文件名
#### （1）  数据1：结果1；…… ; 数据5：结果5；
#### （2）  计算对象简单校验和: ****；

See [Mingzhe's implementation](https://github.com/DuNGEOnmassster/Computer_Network_Homework/tree/mingzhe/Project1) and [Zhengbao's implementation](https://github.com/DuNGEOnmassster/Computer_Network_Homework/tree/zhengbao/Project1)