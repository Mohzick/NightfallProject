#include "stdafx.h"
#include <stdio.h>
#include <winsock2.h>
#include "windows.h"
#include "robot.h"
#include <iostream>

using namespace std;

//Contorlling RS232C
#define ASCII_BEL       0x07
#define ASCII_BS        0x08
#define ASCII_LF        0x0A
#define ASCII_CR        0x0D
#define ASCII_XON       0x11
#define ASCII_XOFF      0x13


HANDLE hCom;

int robot(char c, unsigned char v)
{
	//WSADATA wsaData;
	//struct sockaddr_in server;
	//SOCKET sock;
	//char buf[32];
	//start initializing RS232C

	const char* comPort;
	comPort = "COM3";
	hCom = CreateFileA(comPort, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL); //setting comport 
	if (hCom == INVALID_HANDLE_VALUE) {
		return 0;
	}
	DCB dcb;
	//BOOL fRetVal ;
	BYTE bSet = 0;
	dcb.DCBlength = sizeof(DCB);
	GetCommState(hCom, &dcb);
	dcb.BaudRate = 115200;		// speed
	dcb.ByteSize = 8;			// data length
	dcb.Parity = NOPARITY;		// parity bit：EVENPARITY,MARKPARITY,NOPARITY,ODDPARITY
	dcb.StopBits = ONESTOPBIT;  // stop bit：ONESTOPBIT,ONE5STOPBITS,TWOSTOPBITS
	dcb.fOutxDsrFlow = bSet;
	if (bSet) {
		dcb.fDtrControl = DTR_CONTROL_HANDSHAKE;
	}
	else {
		dcb.fDtrControl = DTR_CONTROL_ENABLE;
	}
	bSet = 0;
	dcb.fInX = dcb.fOutX = bSet;
	dcb.XonChar = ASCII_XON;
	dcb.XoffChar = ASCII_XOFF;
	dcb.XonLim = 100;
	dcb.XoffLim = 100;
	dcb.fBinary = TRUE;
	dcb.fParity = TRUE;
	SetCommState(hCom, &dcb);
	//end initializing RS232c
	/*
	// init winsock2
	WSAStartup(MAKEWORD(2,0), &wsaData);
	// create socket
	sock = socket(AF_INET, SOCK_STREAM, 0);

	server.sin_family = AF_INET;
	server.sin_port = htons(12345);
	server.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	//connecting server
	connect(sock, (struct sockaddr *)&server, sizeof(server));
	// receiving data from server
	while(1){
	memset(buf, 0, sizeof(buf));
	int n = recv(sock, buf, sizeof(buf), 0);
	printf("%d, %s\n", n, buf);
	}
	// clean up winsock2
	WSACleanup();
	*/
	start();
	if (c == 'f') foward(v); //v is velocity
	else if (c == 'b') back();
	else if (c == 'r') right(v);
	else if (c == 'l') left(v);
	else if (c == 's') stop();
	//clean up
	CloseHandle(hCom);

	return 0;
}
void start() {
	unsigned char send[2];
	unsigned long len;

	send[0] = 128; //命令を送る前に128 131というコマンドを送ってiRobotを始動させる sending 128 131 is to weake up iRobot,  
	send[1] = 132; //131はsafemodeだった   131 is safemode. 
	WriteFile(hCom, send, 2, &len, NULL);
	// printf("%d %d\n", send[0], send[1]);
}
void foward(unsigned char v) {
	unsigned char send[5];
	unsigned long len;
	send[0] = 137;
	send[1] = 0;
	send[2] = 500; //速度指定
	send[3] = 128;
	send[4] = 0; //send[3],send[4]で方向の指定、128 0は前後方向  Set speed to send[1] send[2]. send[3][5] is related to direction. 128 0 means "go straight"
	WriteFile(hCom, send, 5, &len, NULL);
	//printf("foward\n");
}
void back() {
	unsigned char send[5];
	unsigned long len;
	send[0] = 137;
	send[1] = 255;
	send[2] = 226; //send[1],send[2]により速度指定、16進数で負の値となるようにする Set speed to send[1] send[2]. Also, to let robot back,  send[1] send[2] are  minus value as Hexadecimal. 
	send[3] = 128;
	send[4] = 0;
	WriteFile(hCom, send, 5, &len, NULL);
	//printf("back\n");
}
void left(unsigned char v) {
	unsigned char send[5];
	unsigned long len;
	send[0] = 137;
	send[1] = 0;
	send[2] = v;
	send[3] = 0;
	send[4] = 1;  //0 1 は左方向 0 1 means left spin turn.
	WriteFile(hCom, send, 5, &len, NULL);
	//printf("right\n");
}
void right(unsigned char v) {
	unsigned char send[5];
	unsigned long len;
	send[0] = 137;
	send[1] = 0;
	send[2] = v;
	send[3] = 255;
	send[4] = 255; //255 255は右方向 255 255 means right spin turn.
	WriteFile(hCom, send, 5, &len, NULL);
	//printf("right\n");
}
void stop() {
	unsigned char send[5];
	unsigned long len;
	send[0] = 137;
	send[1] = 0;
	send[2] = 0; //速度0でストップ Set speed to 0. It means stop
	send[3] = 128;
	send[4] = 0;
	WriteFile(hCom, send, 5, &len, NULL);
	//printf("stop\n");
}

