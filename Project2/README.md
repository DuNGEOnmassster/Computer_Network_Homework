# Project for the 2nd

题目：数据链路层网络通信协议设计 

 要求：数据链路层通信的可靠性，非可靠性；具体用 户自己选择； 

 可靠性分析：

 （1）差错控制：检错（CRC-32）;纠错 （序号+确认反馈+超时重发）；

 （2）流量控制：采 用选择重发协议（序号为3个比特位，发送缓冲区和接 收缓存区，确定发送窗口和接收窗口，对缓冲区和窗 口管理）

 不可靠性分析：支持不可靠通信服务(没有序号)。 
 
 协议设计分析：语法，语义和同步

 See [Mingzhe's implementation](https://github.com/DuNGEOnmassster/Computer_Network_Homework/tree/mingzhe/Project2) and [Zhengbao's implementation](https://github.com/DuNGEOnmassster/Computer_Network_Homework/tree/zhengbao/Project2)