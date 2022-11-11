import socket
import time
import argparse
import os
import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description="TCP socket")

    parser.add_argument("--server_host", default="127.0.0.1",
                        help="declare server ip address")
    parser.add_argument("--host", default="10.31.51.162",
                        help="declare client ip address")
    parser.add_argument("--port", type=int, default=5001,
                        help="declare port")
    parser.add_argument("--client_num", type=int, default=5,
                        help="declare the maximum num of client")
    parser.add_argument("--buffer_size", type=int, default=4096,
                        help="send 4096 bytes each time step")

    parser.add_argument("--send_text", type=bool, default=False,
                        help="flag determine whether to send text (defualt: False)")
    parser.add_argument("--send_file", type=bool, default=True,
                        help="flag determine whether to send file (defualt: True)")
    parser.add_argument("--filename", type=str, default="./test.txt",
                        help="declare file to be sent")
    parser.add_argument("--sent_addr", type=str, default="/Users/normanz/Desktop/Github/Computer_Network_Homework/ex1/data",
                        help="declare where the file will be sent to")

    return parser.parse_args()


def tcp_server(args):
    # create the server socket
    # TCP socket
    s = socket.socket()

if __name__ == "__main__":
    args = parse_args()
    tcp_server(args)


