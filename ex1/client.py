import socket
import os
import tqdm
from server import args


def Client(args):
    protocol = "TCP" if args.TCP else "UDP"
    # create the client socket
    if args.TCP:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c.connect((args.server_host, args.server_port))
    print(f"[+] Connecting to {args.server_host}:{args.server_port}")
    print(f"[+] Connected in {protocol}.")
    if args.send_file:
        # send the filename and filesize
        filesize = os.path.getsize(args.filename)
        c.send(f"{args.filename}{args.SEPARATOR}{filesize}".encode())
    
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {args.filename}", unit="B", unit_scale=True, unit_divisor=args.BUFFER_SIZE)
        with open(args.filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(args.BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                
                if args.TCP:
                    # TCP use sendall to assure transimission in busy networks
                    c.sendall(bytes_read)
                else:
                    # UDP use sendto to assure transimission without listening and accepting
                    c.sendto(bytes_read, (args.server_host, args.server_port))
                # update the progress bar
                progress.update(len(bytes_read))
                
        # print(f"Restore in {args.receive_path + args.filename}")
        # close the socket
        c.close()
    
    elif args.send_text:
        while True:
            send_data=input("Enter message be sent to server: ")
            c.send(send_data.encode("utf-8"))
            return_data = c.recv(args.BUFFER_SIZE).decode("utf-8")
            print(f"Receive message from server: {return_data}")
            if send_data == "exit" or return_data == "exit":
                break

    else:
        print("Failed to send file or text script, check parameters")

if __name__ == "__main__":
    Client(args)


