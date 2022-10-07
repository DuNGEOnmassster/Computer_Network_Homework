from socket import socket, AF_INET, SOCK_STREAM
import time

# 设置超参数
server_ip = "192.168.31.74"  # 定义本地IPv4地址
client_num = 5  # 定义最大连接client数量
port_id = 8003  # 定义端口号，8000为默认端口号

# 创建套接字
tcp_server = socket(AF_INET, SOCK_STREAM)
# 用bind建立长期会话连接
tcp_server.bind((server_ip, port_id))
# 设置监听
tcp_server.listen(client_num)
# 阻塞连接
# client_socket用来为这个客户端服务，相当于的tcp_server套接字的代理
# clientAddr存放的就是连接服务器的客户端地址
client_socket, clientAddr = tcp_server.accept()

while True:
    #接收对方发送过来的数据
    data = client_socket.recv(1024)
    print("收到client信息：" + data.decode('utf-8'))
    if(data=="exit"): # 断开连接
        print("通信结束")
        break
    send_data = input("请输入返回给client的信息：")
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    client_socket.send((str(now_time)+send_data).encode('utf-8'))
    
# 通信完毕后，关闭套接字
client_socket.close()
