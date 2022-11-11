import socket
import argparse
import os
import tqdm
from server import parse_args


def tcp_client(args):
    # create the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {args.host}:{args.port}")
    s.connect((args.host, args.port))
    print("[+] Connected.")
    if args.send_file:
        # send the filename and filesize
        SEPARATOR = "<SEPARATOR>"
        filesize = os.path.getsize(args.filename)
        s.send(f"{args.filename}{SEPARATOR}{filesize}".encode())
    
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {args.filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(args.filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(args.BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        s.close()

if __name__ == "__main__":
    args = parse_args()
    tcp_client(args)


