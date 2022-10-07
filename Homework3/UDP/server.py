from socket import *

# 设置超参数
server_ip = "192.168.31.74"  # 定义本地IPv4地址
port_id = 50002  # 定义端口号

# 创建套接字（会话对象）
udp_server = socket(AF_INET, SOCK_STREAM)

# 建立连接
udp_server.bind((server_ip, port_id))
# UDP无监听与阻塞

while True:
    # 接收对方发送过来的数据
    from_client_msg, client_addr = udp_server.recvfrom(1024)
    print("收到client信息: ",from_client_msg.decode("utf-8"))
    if(from_client_msg=="exit"): # 断开连接
        print("通信结束")
        break
    else:# 发送数据给客户端
        send_data = input("输入发送给client的信息: ")
        udp_server.sendto(send_data.encode("utf-8"), client_addr)
    
# 通信完毕后，关闭套接字
udp_server.close()
