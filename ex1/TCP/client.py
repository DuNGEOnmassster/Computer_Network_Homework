import socket
import os
import tqdm
from server import parse_args


def tcp_client(args):
    # create the client socket
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {args.host}:{args.port}")
    c.connect((args.host, args.port))
    print("[+] Connected.")
    if args.send_file:
        # send the filename and filesize
        filesize = os.path.getsize(args.filename)
        c.send(f"{args.filename}{args.SEPARATOR}{filesize}".encode())
    
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
                c.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
                
        # print(f"Restore in {args.receive_path + args.filename}")
        # close the socket
        c.close()
    
    elif args.send_text:
        while True:
            send_data=input("Enter message be sent to server: ")
            c.send(send_data.encode("utf-8"))
            return_data = c.recv(1024).decode("utf-8") # 接收服务端的答复
            print(f"Receive message from server: {return_data}")
            if send_data == "exit":
                break

    else:
        print("Failed to send file or text script, check parameters")

if __name__ == "__main__":
    args = parse_args()
    tcp_client(args)


