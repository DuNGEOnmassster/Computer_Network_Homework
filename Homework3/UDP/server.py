from socket import SOCK_DGRAM, socket, AF_INET
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="TCP server")

    parser.add_argument("--server_ip", default="192.168.31.74",
                        help="declear server ip")
    parser.add_argument("--port", default=50002,
                        help="declear connect port")
    parser.add_argument("--client_num", default=5,
                        help="declear the max num of client at the same time")
    
    return parser.parse_args()


def connect():
    args = parse_args()
    # create key
    server = socket(AF_INET, SOCK_DGRAM)
    # bind
    server.bind((args.server_ip, args.port))

    while True:
        data, addr = server.recvfrom(1024)
        print("收到client信息：" + data.decode('utf-8'))
        send_data = input("请输入返回给client的信息：").encode('utf-8')
        server.sendto(send_data, addr)

        if data == "quit":
            server.close()
            break

if __name__ == "__main__":
    connect()
