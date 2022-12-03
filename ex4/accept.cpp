#include "windows.h"
//#include "paeseICMP.h"

#include<stdio.h>

#include<winsock2.h>
#include<ws2tcpip.h>
#include<iostream>
#include<stdlib.h> 
using namespace std;

#pragma comment (lib, "ws2_32.lib")

#define  BUFFER_SIZE 65536		//设置接收数据包的缓冲区长度

/* ICMP 类型 */
#define ICMP_TYPE_ECHO          8
#define ICMP_TYPE_ECHO_REPLY    0


struct icmp_hdr
{   
    unsigned char type;   /* 类型 */
    unsigned char code;         /* 代码 */
    unsigned short checksum;    /* 校验和 */
    unsigned short id;          /* 标识符 */
    unsigned short seq;         /* 序列号 */
};

//定义IP首部数据结构
typedef struct _IP_HEADER
{
	union 
	{
		BYTE Version;		//版本（前四位）
		BYTE HdrLen;		//IHL（后四位），IP头的长度
	};
	
	BYTE ServiceType;		//服务类型
	WORD TotalLen;			//总长度
	WORD ID;				//标识

	union 
	{
		WORD Flags;			//(前三位)标志
		WORD FragOff;		//(后十三位)分段偏移
	};
	
	BYTE TimeToLive;		//TTL
	BYTE Protocol;			//协议
	
	WORD HdrChksum;			//头校验和
	DWORD SrcAddr;			//源地址
	DWORD DstAddr;			//目的地址
	//BYTE Options;			//选项
	icmp_hdr icmp_hdr;

}IP_HEADER;


//逐步解析ICMP头中的信息

void getIHL(BYTE b, BYTE &result)
{
	result = (b & 0x0f) * 4;
}


void icmpprase(char * buffer)
{
	IP_HEADER ip = *(IP_HEADER *) buffer;

	if((ip.Protocol) == 1)
	{
		struct icmp_hdr icmp_hdr;
		icmp_hdr=ip.icmp_hdr;
		if(icmp_hdr.type ==ICMP_TYPE_ECHO)
		{
			printf("ICMP报文解析：\n");
			printf("源地址%s：\n",inet_ntoa(*(in_addr*)&ip.SrcAddr));
			printf("目的地址%s：\n",inet_ntoa(*(in_addr*)&ip.DstAddr));
			printf("type: %d\n",icmp_hdr.type);
			printf("code: %d\n", icmp_hdr.code);
			printf("checksum: 0x%x\n",icmp_hdr.checksum);
			printf("id: %d\n",icmp_hdr.id);
			printf("seq: %d\n",icmp_hdr.seq);
			printf("\n\n\n\n");
		}
	}
}

int main(int argc, char * argv[])
{
	
	WSADATA wsData;
	//如果程序初始化失败，那么程序退出
	if(WSAStartup(MAKEWORD(2, 2), &wsData) != 0)
	{
		cout << "WSAStartup failed" << endl;
		return -1;
	}
	
	//建立原始SOCKET
	SOCKET sock;
	if((sock = socket(AF_INET, SOCK_RAW, IPPROTO_IP)) == INVALID_SOCKET)
	{
		cout << "CREATE SOCKET FAILED" << endl;
		return -1;
	}
	
	//设置IP头操作选项，其中flag设为TURE， 用户可以亲自对IP头进行处理
	BOOL flag = TRUE;
	if(setsockopt(sock, IPPROTO_IP, IP_HDRINCL, (char*) & flag, sizeof(flag)) == SOCKET_ERROR)
	{
		cout << "setsockopt failed" << endl;
		return -1;
	}
	
	char hostName[128];
	if(gethostname(hostName, 100) == SOCKET_ERROR)
	{
		cout << "gethostName failed" << endl;
		return -1;
	}
	
	//获取本机IP地址
	hostent * pHostIP;
	if((pHostIP = gethostbyname(hostName)) == NULL)
	{
		cout << "gethostbyname failed" << endl;
		return -1;
	}
	
	//填充SOCKADDR_IN结构
	sockaddr_in addr_in;
	addr_in.sin_addr = *(in_addr*) pHostIP -> h_addr_list[0];
	addr_in.sin_family = AF_INET;
	addr_in.sin_port = htons(6000);
	
	//把原始的socket绑定到网卡
	if(bind (sock, (PSOCKADDR) & addr_in, sizeof(addr_in)) == SOCKET_ERROR)
	{
		cout << "bind failed" << endl;
		return -1;
	}
	DWORD dwValue = 1;
	
	//设置SOCK_RAW为SIO_RCVALL, 以便接收所有的IP包
	#define IO_RCVALL _WSAIOW (IOC_VENDOR, 1)
	DWORD dwBufferLen[10];
	DWORD dwBufferInLen = 1;
	DWORD dwBytesReturned = 0;
	
	if(WSAIoctl (sock, IO_RCVALL, &dwBufferInLen, sizeof(dwBufferInLen), &dwBufferLen, sizeof(dwBufferLen), &dwBytesReturned, NULL, NULL) == SOCKET_ERROR)
	{
		cout << "ioctlsocket failed" << endl;
		return -1;
	}
	
	//设置接收数据包的缓冲区长度
	char buffer[BUFFER_SIZE];
	
	//监听网卡
	cout << "开始解析经过本机的ICMP数据包" << endl << endl;
	
	while (true)
	{
		int size = recv(sock, buffer, BUFFER_SIZE, 0);
		if(size > 0)
		{
			icmpprase(buffer);
		}
	}
	return 0;
}

