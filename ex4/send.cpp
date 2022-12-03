

#include <stdio.h>
#include <winsock2.h>
#include <windows.h>
#include<stdlib.h> 
#pragma comment(lib, "ws2_32.lib")    /* WinSock使用的库函数 */

/* ICMP 类型 */
#define ICMP_TYPE_ECHO          8
#define ICMP_TYPE_ECHO_REPLY    0

#define ICMP_MIN_LEN            8  /* ICMP 最小长度, 只有首部 */
#define ICMP_DEF_COUNT          4  /* 缺省数据次数 */
#define ICMP_DEF_SIZE          32  /* 缺省数据长度 */
#define ICMP_DEF_TIMEOUT     1000  /* 缺省超时时间, 毫秒 */
#define ICMP_MAX_SIZE       65500  /* 最大数据长度 */

/* IP 首部 -- RFC 791 */
struct ip_hdr
{
    unsigned char vers_len;     /* 版本和首部长度 */
    unsigned char tos;          /* 服务类型 */
    unsigned short total_len;   /* 数据报的总长度 */
    unsigned short id;          /* 标识符 */
    unsigned short frag;        /* 标志和片偏移 */
    unsigned char ttl;          /* 生存时间 */
    unsigned char proto;        /* 协议 */
    unsigned short checksum;    /* 校验和 */
    unsigned int sour;          /* 源 IP 地址 */
    unsigned int dest;          /* 目的 IP 地址 */
};

/* ICMP 首部 -- RFC 792 */
struct icmp_hdr
{   
    unsigned char type;         /* 类型 */
    unsigned char code;         /* 代码 */
    unsigned short checksum;    /* 校验和 */
    unsigned short id;          /* 标识符 */
    unsigned short seq;         /* 序列号 */
    
    /* 这之后的不是标准 ICMP 首部, 用于记录时间 */
    unsigned long timestamp;
};

struct icmp_user_opt
{
    unsigned int  persist;  /* 一直 Ping            */
    unsigned int  count;    /* 发送 ECHO 请求的数量 */
    unsigned int  size;     /* 发送数据的大小       */
    unsigned int  timeout;  /* 等待答复的超时时间   */
    char          *host;    /* 主机地址     */
    unsigned int  send;     /* 发送数量     */
    unsigned int  recv;     /* 接收数量     */
    unsigned int  min_t;    /* 最短时间     */
    unsigned int  max_t;    /* 最长时间     */
    unsigned int  total_t;  /* 总的累计时间 */
};

/* 随机数据 */
const char icmp_rand_data[] = "abcdefghigklmnopqrstuvwxyz0123456789"
                                "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

struct icmp_user_opt user_opt_g = { 
      0, ICMP_DEF_COUNT, ICMP_DEF_SIZE, ICMP_DEF_TIMEOUT, NULL,
      0, 0, 0xFFFF, 0
    };

unsigned short ip_checksum(unsigned short *buf, int buf_len);


/**************************************************************************
 *
 * 函数功能: 构造 ICMP 数据.
 *
 * 参数说明: [IN, OUT] icmp_data, ICMP 缓冲区;
 *           [IN] data_size, icmp_data 的长度;
 *           [IN] sequence, 序列号.
 *
 * 返 回 值: void.
 *
 **************************************************************************/
void icmp_make_data(char *icmp_data, int data_size, int sequence)
{   
    struct icmp_hdr *icmp_hdr;
    char *data_buf;
    int data_len;
    int fill_count = sizeof(icmp_rand_data) / sizeof(icmp_rand_data[0]);

    /* 填写 ICMP 数据 */
    data_buf = icmp_data + sizeof(struct icmp_hdr);
    data_len = data_size - sizeof(struct icmp_hdr);
    
    while (data_len > fill_count)
    {
        memcpy(data_buf, icmp_rand_data, fill_count);
        data_len -= fill_count;
    }

    if (data_len > 0)
        memcpy(data_buf, icmp_rand_data, data_len);

    /* 填写 ICMP 首部 */
    icmp_hdr = (struct icmp_hdr *)icmp_data;

    icmp_hdr->type = ICMP_TYPE_ECHO;
    icmp_hdr->code = 0;
    icmp_hdr->id = (unsigned short)GetCurrentProcessId();
    icmp_hdr->checksum = 0;
    icmp_hdr->seq = sequence;
    icmp_hdr->timestamp = GetTickCount();

    icmp_hdr->checksum = ip_checksum((unsigned short*)icmp_data, data_size);

	printf(">> ICMP Data Decomposition:\n");
	printf("ICMP Type: %d\n",icmp_hdr->type);
	printf("ICMP Code: %d\n",icmp_hdr->code);
	printf("ICMP CheckSum: 0x%4x\n",icmp_hdr->checksum);
	printf("ICMP ID: %d\n",icmp_hdr->id);
	printf("ICMP Sequence: %d\n",icmp_hdr->seq);
	printf(">> Decomposition Accomplished!\n\n");

}

/**************************************************************************
 *
 * 函数功能: 解析接收到的数据.
 *
 * 参数说明: [IN] buf, 数据缓冲区;
 *           [IN] buf_len, buf 的长度;
 *           [IN] from, 对方的地址.
 *
 * 返 回 值: 成功返回 0, 失败返回 -1.
 *
 **************************************************************************/
int icmp_parse_reply(char *buf, int buf_len,struct sockaddr_in *from)
{
    struct ip_hdr *ip_hdr;
    struct icmp_hdr *icmp_hdr;
    unsigned short hdr_len;
    int icmp_len;
    unsigned long trip_t;

    ip_hdr = (struct ip_hdr *)buf;
    hdr_len = (ip_hdr->vers_len & 0xf) << 2 ; /* IP 首部长度 */

    if (buf_len < hdr_len + ICMP_MIN_LEN)
    {    
        printf("[Ping] Too few bytes from %s\n", inet_ntoa(from->sin_addr));
        return -1;
    }

    icmp_hdr = (struct icmp_hdr *)(buf + hdr_len);
    icmp_len = ntohs(ip_hdr->total_len) - hdr_len;

    /* 检查校验和 */
    if (ip_checksum((unsigned short *)icmp_hdr, icmp_len))
    {
        printf("[Ping] icmp checksum error!\n");
        return -1;
    }

    /* 检查 ICMP 类型 */
    if (icmp_hdr->type != ICMP_TYPE_ECHO_REPLY)
    {    
        printf("[Ping] not echo reply : %d\n", icmp_hdr->type);
        return -1;
    }

    /* 检查 ICMP 的 ID */
    if (icmp_hdr->id != (unsigned short)GetCurrentProcessId())
    {    
        printf("[Ping] someone else's message!\n");
        return -1;    
    } 

    /* 输出响应信息 */
    trip_t = GetTickCount() - icmp_hdr->timestamp;
    buf_len = ntohs(ip_hdr->total_len) - hdr_len - ICMP_MIN_LEN;
    printf("%d bytes from %s:", buf_len, inet_ntoa(from->sin_addr));
    printf(" icmp_seq = %d  time: %d ms\n",icmp_hdr->seq, trip_t);

    user_opt_g.recv++;
    user_opt_g.total_t += trip_t;

    /* 记录返回时间 */
    if (user_opt_g.min_t > trip_t)
        user_opt_g.min_t = trip_t;

    if (user_opt_g.max_t < trip_t)
        user_opt_g.max_t = trip_t;

    return 0;
}

/**************************************************************************
 *
 * 函数功能: 接收数据, 处理应答.
 *
 * 参数说明: [IN] icmp_soc, 套接口描述符.
 *
 * 返 回 值: 成功返回 0, 失败返回 -1.
 *
 **************************************************************************/
int icmp_process_reply(SOCKET icmp_soc)
{
    struct sockaddr_in from_addr;
    int result, data_size = user_opt_g.size;
    int from_len = sizeof(from_addr);
    char *recv_buf;

    data_size += sizeof(struct ip_hdr) + sizeof(struct icmp_hdr);
    recv_buf = (char*)malloc(data_size);

    /* 接收数据 */
    result = recvfrom(icmp_soc, recv_buf, data_size, 0,
                      (struct sockaddr*)&from_addr, &from_len);
    if (result == SOCKET_ERROR)
    {    
        if (WSAGetLastError() == WSAETIMEDOUT)
            printf("timed out\n");
        else
            printf("[PING] recvfrom_ failed: %d\n", WSAGetLastError());
        
        return -1;
    } 

    result = icmp_parse_reply(recv_buf, result, &from_addr);
    free(recv_buf);

    return result;
}

/**************************************************************************
 *
 * 函数功能: 显示 ECHO 的帮助信息.
 *
 * 参数说明: [IN] prog_name, 程序名;
 *
 * 返 回 值: void.
 *
 **************************************************************************/
void icmp_help(char *prog_name)
{
    char *file_name;

    file_name = strrchr(prog_name, '\\');
    if (file_name != NULL)
        file_name++;
    else
        file_name = prog_name;

    /* 显示帮助信息 */
    printf(" usage:     %s host_address [-t] [-n count] [-l size] "
           "[-w timeout]\n", file_name);
    printf(" -t         Ping the host until stopped.\n");
    printf(" -n count   the count to send ECHO\n");
    printf(" -l size    the size to send data\n");
    printf(" -w timeout timeout to wait the reply\n");
    exit(1);
}

/**************************************************************************
 *
 * 函数功能: 解析命令行选项, 保存到全局变量中.
 *
 * 参数说明: [IN] argc, 参数的个数;
 *           [IN] argv, 字符串指针数组.
 *
 * 返 回 值: void.
 *
 **************************************************************************/
void icmp_parse_param(int argc, char **argv)
{
    int i;

    for(i = 1; i < argc; i++)
    {
        if ((argv[i][0] != '-') && (argv[i][0] != '/'))
        {   
            /* 处理主机名 */
            if (user_opt_g.host)
                icmp_help(argv[0]);
            else
            {
                user_opt_g.host = argv[i];
                continue;
            }
        }

        switch (tolower(argv[i][1]))
        {
        case 't':   /* 持续 Ping */
            user_opt_g.persist = 1;
            break;

        case 'n':   /* 发送请求的数量 */
            i++;    
            user_opt_g.count = atoi(argv[i]);
            break;

        case 'l':   /* 发送数据的大小 */
            i++;    
            user_opt_g.size = atoi(argv[i]);
            if (user_opt_g.size > ICMP_MAX_SIZE)
                user_opt_g.size = ICMP_MAX_SIZE;
            break;

        case 'w':   /* 等待接收的超时时间 */
            i++;    
            user_opt_g.timeout = atoi(argv[i]);
            break;

        default:
            icmp_help(argv[0]);
            break;
        }
    }
}


int main(int argc, char **argv)
{
    WSADATA wsaData;
    SOCKET icmp_soc;
    struct sockaddr_in dest_addr;
    struct hostent *host_ent = NULL;
    
    int result, data_size, send_len;
    unsigned int i, timeout, lost;
    char *icmp_data;
    unsigned int ip_addr = 0;
    unsigned short seq_no = 0;

    if (argc < 2) 
        icmp_help(argv[0]);

    icmp_parse_param(argc, argv);
    WSAStartup(MAKEWORD(2,0),&wsaData);

    /* 解析主机地址 */
    ip_addr = inet_addr(user_opt_g.host);
    if (ip_addr == INADDR_NONE)
    {
        host_ent = gethostbyname(user_opt_g.host);
        if (!host_ent)
        {
            printf("[PING] Fail to resolve %s\n", user_opt_g.host);
            return -1;
        }
        
        memcpy(&ip_addr, host_ent->h_addr_list[0], host_ent->h_length);
    }

    icmp_soc = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (icmp_soc == INVALID_SOCKET)
    {    
        printf("[PING] socket() failed: %d\n", WSAGetLastError());
        return -1;
    }

	

    /* 设置选项, 接收和发送的超时时间　*/
    timeout = user_opt_g.timeout;
    result = setsockopt(icmp_soc, SOL_SOCKET, SO_RCVTIMEO,
                        (char*)&timeout, sizeof(timeout));

    timeout = 1000;
    result = setsockopt(icmp_soc, SOL_SOCKET, SO_SNDTIMEO,
                        (char*)&timeout, sizeof(timeout));

    memset(&dest_addr,0,sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_addr.s_addr = ip_addr;

    data_size = user_opt_g.size + sizeof(struct icmp_hdr) - sizeof(long);
    icmp_data = (char*)malloc(data_size);

    if (host_ent)
        printf("Ping %s [%s] with %d bytes data\n", user_opt_g.host,
            inet_ntoa(dest_addr.sin_addr), user_opt_g.size);
    else
        printf("Ping [%s] with %d bytes data\n", inet_ntoa(dest_addr.sin_addr),
            user_opt_g.size);

	

    /* 发送请求并接收响应 */
    for (i = 0; i < user_opt_g.count; i++)
    {
        icmp_make_data(icmp_data, data_size, seq_no++);
      
        send_len = sendto(icmp_soc, icmp_data, data_size, 0, 
                          (struct sockaddr*)&dest_addr, sizeof(dest_addr));

		//ICMP_decomposition(icmp_data);

        if (send_len == SOCKET_ERROR)
        {
            if (WSAGetLastError() == WSAETIMEDOUT)
            {
                printf("[PING] sendto is timeout\n");
                continue;
            }

            printf("[PING] sendto failed: %d\n", WSAGetLastError());
            break;
        } 

		
        user_opt_g.send++;
        result = icmp_process_reply(icmp_soc);

        user_opt_g.persist ? i-- : i; /* 持续 Ping */
        Sleep(1000); /* 延迟 1 秒 */
    }    

    lost = user_opt_g.send - user_opt_g.recv;

    /* 打印统计数据 */
    printf("\nStatistic :\n");
    printf("    Packet : sent = %d, recv = %d, lost = %d (%3.f%% lost)\n", 
      user_opt_g.send, user_opt_g.recv, lost, (float)lost*100/user_opt_g.send);

    if (user_opt_g.recv > 0)
    {
        printf("Roundtrip time (ms)\n");
        printf("    min = %d ms, max = %d ms, avg = %d ms\n", user_opt_g.min_t,
            user_opt_g.max_t, user_opt_g.total_t / user_opt_g.recv);
    }

    free(icmp_data);
    closesocket(icmp_soc);
    WSACleanup();

    return 0;
}
  
/**************************************************************************
 *
 * 函数功能: 计算校验和.
 *
 * 参数说明: [IN] buf, 数据缓冲区;
 *           [IN] buf_len, buf 的字节长度.
 *
 * 返 回 值: 校验和.
 *
 **************************************************************************/
unsigned short ip_checksum(unsigned short *buf, int buf_len)
{
    unsigned long checksum = 0;

    while (buf_len > 1)
    {
        checksum += *buf++;
        buf_len -= sizeof(unsigned short);
    }

    if (buf_len)
    {
        checksum += *(unsigned char *)buf;
    }

    checksum = (checksum >> 16) + (checksum & 0xffff);
    checksum += (checksum >> 16);

    return (unsigned short)(~checksum);
}
