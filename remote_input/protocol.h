#ifndef _PROTOCOL_H
#define _PROTOCOL_H

#define PROTOCOL_CONTROL	1
#define PROTOCOL_TOUCH		2
#define PROTOCOL_KEY		3
#define PROTOCOL_MOUSE		4
#define PROTOCOL_LOCATION	5
#define PROTOCOL_TEST		6

#define MAX_SENSOR_TYPE		13

#define CONTROL_CMD_UDP_PORT	1
#define CONTROL_CMD_SENSOR		2
#define CONTROL_CMD_LOCAION		3
#define CONTROL_CMD_KEY			4
#define CONTROL_CMD_MOUSE		5
#define CONTROL_CMD_TOUCH		6

#define DIRECT_FROM_CLIENT	1
#define DIRECT_FROM_SERVER	2

#pragma pack(1)

struct control_data
{
	short cmd;
	short direct;
	union
	{
		char b8[32];
		short b16[16];
		int b32[8];
	} argv;
	short ret;
};

struct sensor_data
{
	short sensor_type;
	float data[3];
};

struct protocol_event
{
	short type;
	union
	{
		struct control_data control;
		struct sensor_data sensor[MAX_SENSOR_TYPE];
		char test[32];
	} packet;
};
#pragma pack()

#endif

