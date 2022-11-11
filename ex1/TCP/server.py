import socket
import time
import argparse
import os
import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description="TCP socket")

    parser.add_argument("--server_host", default="0.0.0.0",
                        help="declare server ip address")
    parser.add_argument("--host", default="10.31.51.162",
                        help="declare client ip address")
    parser.add_argument("--port", type=int, default=5001,
                        help="declare port")
    parser.add_argument("--client_num", type=int, default=5,
                        help="declare the maximum num of client")
    parser.add_argument("--BUFFER_SIZE", type=int, default=4096,
                        help="send 4096 bytes each time step")
    parser.add_argument("--SEPARATOR", type=str, default="SEPARATOR",
                        help="declare SEPARATOR")

    parser.add_argument("--send_text", type=bool, default=False,
                        help="flag determine whether to send text (defualt: False)")
    parser.add_argument("--send_file", type=bool, default=True,
                        help="flag determine whether to send file (defualt: True)")
    parser.add_argument("--filename", type=str, default="./../data/1111.avi",
                        help="declare file to be sent")

    return parser.parse_args()


def tcp_server(args):
    # create the server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to our local address
    s.bind((args.server_host, args.port))
    # enabling our server to accept connections
    s.listen(args.client_num)
    print(f"[*] Listening as {args.server_host}:{args.port}")

    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    if args.send_file:
        # receive the file infos
        # receive using client socket, not server socket
        received = client_socket.recv(args.BUFFER_SIZE).decode()
        filename, filesize = received.split(args.SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)[:-1]
        filesize = 985 if ">" in filesize else int(filesize)
        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(int(filesize)), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(args.BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        # close the client socket
        client_socket.close()
        # close the server socket
        s.close()


if __name__ == "__main__":
    args = parse_args()
    tcp_server(args)


