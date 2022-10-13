from server import parse_args
from socket import SOCK_DGRAM, socket, AF_INET


def connect():
    args = parse_args()
    # create key
    client = socket(AF_INET, SOCK_DGRAM)
    # send
    while True:
        data = input("请输入给server的信息：").encode('utf-8')
        client.sendto(data, (args.server_ip, args.port)) # 转码
        back_data = client.recvfrom(1024)
        print("server返回了："+back_data[0].decode('utf_8'))

        if data == "quit":
            break

if __name__ == "__main__":
    connect()