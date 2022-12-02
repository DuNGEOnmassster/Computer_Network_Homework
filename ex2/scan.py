from socket import *

def portScanner(host,port, busy):
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        print('[+] %d open' % port)
        busy.append(port)
        s.close()
    except:
        print('[-] %d close' % port)

def main():
    busy = []
    setdefaulttimeout(0.1)
    for p in range(1,1024):
        portScanner('192.168.31.74',p, busy)
    print(busy)

if __name__ == '__main__':
    main()
