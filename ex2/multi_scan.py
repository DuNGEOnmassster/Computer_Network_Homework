from socket import *
import threading

lock = threading.Lock()
openNum = 0
threads = []

def portScanner(host,port):
    global openNum
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        lock.acquire()
        openNum+=1
        print('[+] %d open' % port)
        lock.release()
        s.close()
    except:
        pass

def main():
    setdefaulttimeout(0.01)
    for p in range(1,1024):
        t = threading.Thread(target=portScanner,args=('192.168.31.74',p))
        threads.append(t)
        t.start()     

    for t in threads:
        t.join()

    print('[*] The scan is complete!')
    print('[*] A total of %d open port ' % (openNum))

if __name__ == '__main__':
    main()