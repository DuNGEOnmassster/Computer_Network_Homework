from socket import socket, AF_INET, SOCK_STREAM
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="TCP server")

    parser.add_argument("--server_ip", default="192.168.31.74",
                        help="declear server ip")
    parser.add_argument("--port", default=8003,
                        help="declear connect port")
    parser.add_argument("--client_num", default=5,
                        help="declear the max num of client at the same time")
    
    return parser.parse_args()


def connect():
    args = parse_args()
    # create key
    server = socket(AF_INET, SOCK_STREAM)
    # bind
    server.bind((args.server_ip, args.port))
    # listen
    server.listen(args.client_num)
    # block
    client_socket, client_addr = server.accept()

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        print("收到client信息：" + data)
        send_data = input("请输入返回给client的信息：").encode('utf-8')
        client_socket.send(send_data)

        if data == "quit":
            server.close()
            break

if __name__ == "__main__":
    connect()
