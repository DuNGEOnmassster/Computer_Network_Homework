#include "windows.h"
//#include "paeseICMP.h"

#include<stdio.h>

#include<winsock2.h>
#include<ws2tcpip.h>
#include<iostream>
#include<stdlib.h> 
using namespace std;

#pragma comment (lib, "ws2_32.lib")

#define  BUFFER_SIZE 65536		//���ý������ݰ��Ļ���������

/* ICMP ���� */
#define ICMP_TYPE_ECHO          8
#define ICMP_TYPE_ECHO_REPLY    0


struct icmp_hdr
{   
    unsigned char type;   /* ���� */
    unsigned char code;         /* ���� */
    unsigned short checksum;    /* У��� */
    unsigned short id;          /* ��ʶ�� */
    unsigned short seq;         /* ���к� */
};

//����IP�ײ����ݽṹ
typedef struct _IP_HEADER
{
	union 
	{
		BYTE Version;		//�汾��ǰ��λ��
		BYTE HdrLen;		//IHL������λ����IPͷ�ĳ���
	};
	
	BYTE ServiceType;		//��������
	WORD TotalLen;			//�ܳ���
	WORD ID;				//��ʶ

	union 
	{
		WORD Flags;			//(ǰ��λ)��־
		WORD FragOff;		//(��ʮ��λ)�ֶ�ƫ��
	};
	
	BYTE TimeToLive;		//TTL
	BYTE Protocol;			//Э��
	
	WORD HdrChksum;			//ͷУ���
	DWORD SrcAddr;			//Դ��ַ
	DWORD DstAddr;			//Ŀ�ĵ�ַ
	//BYTE Options;			//ѡ��
	icmp_hdr icmp_hdr;

}IP_HEADER;


//�𲽽���ICMPͷ�е���Ϣ

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
			printf("ICMP���Ľ�����\n");
			printf("Դ��ַ%s��\n",inet_ntoa(*(in_addr*)&ip.SrcAddr));
			printf("Ŀ�ĵ�ַ%s��\n",inet_ntoa(*(in_addr*)&ip.DstAddr));
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
	//��������ʼ��ʧ�ܣ���ô�����˳�
	if(WSAStartup(MAKEWORD(2, 2), &wsData) != 0)
	{
		cout << "WSAStartup failed" << endl;
		return -1;
	}
	
	//����ԭʼSOCKET
	SOCKET sock;
	if((sock = socket(AF_INET, SOCK_RAW, IPPROTO_IP)) == INVALID_SOCKET)
	{
		cout << "CREATE SOCKET FAILED" << endl;
		return -1;
	}
	
	//����IPͷ����ѡ�����flag��ΪTURE�� �û��������Զ�IPͷ���д���
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
	
	//��ȡ����IP��ַ
	hostent * pHostIP;
	if((pHostIP = gethostbyname(hostName)) == NULL)
	{
		cout << "gethostbyname failed" << endl;
		return -1;
	}
	
	//���SOCKADDR_IN�ṹ
	sockaddr_in addr_in;
	addr_in.sin_addr = *(in_addr*) pHostIP -> h_addr_list[0];
	addr_in.sin_family = AF_INET;
	addr_in.sin_port = htons(6000);
	
	//��ԭʼ��socket�󶨵�����
	if(bind (sock, (PSOCKADDR) & addr_in, sizeof(addr_in)) == SOCKET_ERROR)
	{
		cout << "bind failed" << endl;
		return -1;
	}
	DWORD dwValue = 1;
	
	//����SOCK_RAWΪSIO_RCVALL, �Ա�������е�IP��
	#define IO_RCVALL _WSAIOW (IOC_VENDOR, 1)
	DWORD dwBufferLen[10];
	DWORD dwBufferInLen = 1;
	DWORD dwBytesReturned = 0;
	
	if(WSAIoctl (sock, IO_RCVALL, &dwBufferInLen, sizeof(dwBufferInLen), &dwBufferLen, sizeof(dwBufferLen), &dwBytesReturned, NULL, NULL) == SOCKET_ERROR)
	{
		cout << "ioctlsocket failed" << endl;
		return -1;
	}
	
	//���ý������ݰ��Ļ���������
	char buffer[BUFFER_SIZE];
	
	//��������
	cout << "��ʼ��������������ICMP���ݰ�" << endl << endl;
	
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
