// Source Reference C code from Project description
#include “stdafx.h”
#include  “math.h”
//定义线程与共享内存
CWinThread *thread1, *thread2;
DWORD ID1, ID2, Bus=0;
UINT aThread(LPVOID  pParam);
UINT bThread(LPVOID  pParam);
using namespace std;
int   _tmain(int argc, THAR* argv[], ICHAR* envp[])
{
    int nRetCode=0;
    If(!AfxWinInit(::GetModuleHandle(NULL),NULL,::GetComma   
    ndLine(),0))
    {
    cerr<<_T(“fatal error:MFC intialization failed”)<<endl;
    nRetCode=1;
    }
    else
    {  //启动线程a和线程b
    thread1= AfxBeginThread(aThread,NULL);
    ID1 = thread1->m_nThreadID; 
    thread2= AfxBeginThread(bThread,NULL);
    ID2 = thread2->m_nThreadID; 
    }//else
    return nRetCode;
}// main-end

