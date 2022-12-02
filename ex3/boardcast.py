from socket import *

def main():
    address = ('255.255.255.255', 6666)
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    message = b'This is broadcase message !'
    s.sendto(message, address)
    s.close()

if __name__=='__main__':
    main()