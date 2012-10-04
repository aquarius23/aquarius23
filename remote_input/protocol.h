#ifndef _PROTOCOL_H
#define _PROTOCOL_H

#define PROTOCOL_CONTROL	1
#define PROTOCOL_TOUCH		2
#define PROTOCOL_KEY		3
#define PROTOCOL_MOUSE		4
#define PROTOCOL_LOCATION	5
#define PROTOCOL_TEST		6

#define MAX_SENSOR_TYPE		13

#pragma pack(1)
struct control_data
{
	short cmd;
	short arg[8];
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
		struct sensor_data sensor[MAX_SENSOR_TYPE];
		char test[32];
	} packet;
};
#pragma pack()

#endif

