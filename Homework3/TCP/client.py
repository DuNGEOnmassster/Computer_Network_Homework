from server import parse_args
from socket import socket, AF_INET, SOCK_STREAM


def connect():
    args = parse_args()
    # create key
    client = socket(AF_INET, SOCK_STREAM)
    # connect
    client.connect((args.server_ip, args.port))

    # send
    while True:
        data = input("请输入给server的信息：").encode('utf-8')
        client.send(data)
        back_data = client.recv(1024).decode('utf-8')
        print("server返回了："+back_data)

        if data == "quit":
            break

if __name__ == "__main__":
    connect()