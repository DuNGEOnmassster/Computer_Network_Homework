from socket import *
import time

# 设置超参数
server_ip = "10.31.10.211"  # 定义本地IPv4地址
port_id = 50002  # 定义端口号

# 创建套接字（会话对象）
udp_server = socket(AF_INET, SOCK_STREAM)
# 创建address元组用于bind建立长期会话连接，其中
address = (server_ip, port_id)
udp_server.bind(address)
# UDP无监听与阻塞

while True:
    #接收对方发送过来的数据
    from_client_msg, client_addr = udp_server.recvfrom(1024)
    print("收到client信息: ",from_client_msg.decode("utf-8"))
    if(from_client_msg=="exit"): # 断开连接
        print("通信结束")
        break

    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    udp_server.send((str(now_time)+" 已收到！").encode("utf-8"))
    #发送数据给客户端
    send_data = input("输入发送给client的信息: ")
    udp_server.sendto(send_data.encode("utf-8"), client_addr)
    
# 通信完毕后，关闭套接字
udp_server.close()
