import platform
import netifaces
import pprint

def Receiver(s):
    with open("data/1111.avi", "wb") as f:
        while True:
            bytes_read = s.recv(1024)
            if not bytes_read:    
                # if nothing received, file transmitting is done
                break
            # write the bytes we just received to file
            f.write(bytes_read)
    s.close()
        
def test():
    platform.system()
    pp = pprint.PrettyPrinter(indent=4)  #这里使用pprint输出会更直观
    
    pp.pprint(netifaces.address_families)
    print(netifaces.interfaces())

    ip_addr = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']
    print(ip_addr)
    # '192.168.0.253'  #返回结果，获取到IPv4地址
    
    netifaces.ifaddresses('en0')[netifaces.AF_PACKET][0]['addr']
    # '00:0c:29:5d:2f:55'  #返回结果，获取到IPv4的MAC地址

if __name__ == "__main__":
    test()
