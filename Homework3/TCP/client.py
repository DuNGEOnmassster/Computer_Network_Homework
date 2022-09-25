from pydoc import cli
from socket import *
from server import server_ip, port_id

# 创建会话对象
client = socket(AF_INET,SOCK_STREAM)
# 建立连接
client.connect((server_ip,port_id))

while True:
    send_data=input("输入发给服务端的信息: ")
    client.send(send_data.encode("utf-8"))
    if send_data == "exit": # 断开连接
        print("通信结束")
        break
    return_data = client.recv(1024).decode("utf-8") # 接收服务端的答复
    print(f"server返回了: {return_data}")

client.close()

