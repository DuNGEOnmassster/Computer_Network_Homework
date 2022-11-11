import socket
import argparse
import os
import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description="TCP and UDP socket")

    parser.add_argument("--TCP_or_UDP", type=bool, default=True,
                        help="Select use TCP(True) or UDP(False),default with True")
    parser.add_argument("--server_host", default="0.0.0.0",
                        help="declare server ip address")
    parser.add_argument("--host", default="10.31.51.162",
                        help="declare client ip address")
    parser.add_argument("--server_port", type=int, default=5001,
                        help="declare server port")
    parser.add_argument("--port", type=int, default=5001,
                        help="declare port")
    parser.add_argument("--client_num", type=int, default=5,
                        help="declare the maximum num of client")
    parser.add_argument("--BUFFER_SIZE", type=int, default=4096,
                        help="send 4096 bytes each time step")
    parser.add_argument("--SEPARATOR", type=str, default="SEPARATOR",
                        help="declare SEPARATOR")

    parser.add_argument("--send_text", type=bool, default=True,
                        help="flag determine whether to send text (defualt: False)")
    parser.add_argument("--send_file", type=bool, default=False,
                        help="flag determine whether to send file (defualt: True)")
    parser.add_argument("--filename", type=str, default="./data/runtu2lion.mp4",
                        help="declare file to be sent")
    parser.add_argument("--receive_path", type=str, default="./receive_data/",
                        help="declare where to save the file sent from server for client")

    return parser.parse_args()


def Server(args):
    protocol = "TCP" if args.TCP_or_UDP else "UDP"
    print(f"[*] Connect with {protocol}")
    # TCP
    if args.TCP_or_UDP:
        # create the server socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to our local address
        s.bind((args.server_host, args.server_port))
        # enabling our server to accept connections
        s.listen(args.client_num)
        print(f"[*] Listening as {args.server_host}:{args.server_port}")
        # accept connection if there is any
        client_socket, client_address = s.accept() 
        # if below code is executed, that means the sender is connected
        print(f"[+] {client_address} is connected.")
    
    # UDP
    else:
        # create the server socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind the socket to our local address
        s.bind((args.server_host, args.server_port))

    # Send file
    if args.send_file:
        # receive message infos
        if args.TCP_or_UDP:
            received = client_socket.recv(args.BUFFER_SIZE).decode()
        else:
            received, client_address = s.recvfrom(args.BUFFER_SIZE)

        filename, filesize = received.split(args.SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        filesize = int(filesize[1:]) if ">" in filesize else int(filesize)
        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(int(filesize)), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                if args.TCP_or_UDP:
                    bytes_read = client_socket.recv(args.BUFFER_SIZE)
                else:
                    bytes_read, client_address = s.recvfrom(args.BUFFER_SIZE)
                if not bytes_read:    
                    # if nothing received, file transmitting is done
                    break
                # write the bytes we just received to file
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
            
            os.system(f"mv {filename} {args.receive_path + filename}")     

        # close the client socket
        client_socket.close()
        # close the server socket
        s.close()

    # Send text
    elif args.send_text:
        # TCP
        if args.TCP_or_UDP:
            while True:
                data = client_socket.recv(args.BUFFER_SIZE)
                print("Receive message from client: " + data.decode('utf-8'))
                send_data = input("Enter message be sent to client: ")
                client_socket.send((send_data).encode('utf-8'))
                if send_data == "exit" or data == "exit":
                    break
        # UDP
        else:
            while True:
                data, client_addr = s.recvfrom(args.BUFFER_SIZE)
                print("Receive message from client: ",data.decode("utf-8"))
                send_data = input("Enter message be sent to client: ")
                s.sendto(send_data.encode("utf-8"), client_addr)
                if send_data == "exit" or data == "exit":
                    break

        if args.TCP_or_UDP:
            # close the client socket in TCP
            client_socket.close()

        # close the server socket
        s.close()

    else:
        print("Failed to send file or text script, check parameters")

# Make sure client and server share the same parameters when alter occurs in terminal
args = parse_args()

if __name__ == "__main__":
    Server(args)


