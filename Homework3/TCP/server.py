from socket import *
import time

# 设置超参数
server_ip = "10.31.10.211"  # 定义本地IPv4地址
client_num = 128  # 定义最大连接client数量
port_id = 8005  # 定义端口号，8000为默认端口号

# 创建套接字（会话对象）
tcp_server = socket(AF_INET, SOCK_STREAM)
# 创建address元组用于bind建立长期会话连接，其中
address = (server_ip, port_id)
tcp_server.bind(address)
# 设置监听
tcp_server.listen(client_num)

# 阻塞连接
# client_socket用来为这个客户端服务，相当于的tcp_server套接字的代理
# clientAddr存放的就是连接服务器的客户端地址
client_socket, clientAddr = tcp_server.accept()

while True:
    #接收对方发送过来的数据
    from_client_msg = client_socket.recv(1024) #接收1024个字节,这里recv接收的不再是元组，区别UDP

    if(from_client_msg=="exit"): # 断开连接
        print("通信结束")
        break

    print("收到client信息: ",from_client_msg.decode("utf-8"))

    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    client_socket.send((str(now_time)+" 已收到！").encode("utf-8"))
    #发送数据给客户端
    send_data = input("输入发送给client的信息: ")
    client_socket.send(send_data.encode("utf-8"))
    

# 通信完毕后，关闭套接字
client_socket.close()
