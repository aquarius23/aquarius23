#include <string.h>
#include "protocol.h"

void cmd_set_udp_port(struct protocol_handle *handle, struct protocol_event *event, unsigned short port)
{
	event->type = PROTOCOL_CONTROL;
	event->packet.control.cmd = CONTROL_CMD_UDP_PORT;
	event->packet.control.direct = DIRECT_FROM_SERVER;
	event->packet.control.argv.b16[0] = port;
}

void cmd_set_sensor_control(struct protocol_handle *handle, struct protocol_event *event, int sensor, int on)
{
	event->type = PROTOCOL_CONTROL;
	event->packet.control.cmd = CONTROL_CMD_SENSOR;
	event->packet.control.direct = DIRECT_FROM_SERVER;
	event->packet.control.argv.b32[0] = 1;
	event->packet.control.argv.b32[1] = sensor;
	event->packet.control.argv.b32[2] = on;
}

void cmd_set_sensor_delay(struct protocol_handle *handle, struct protocol_event *event, int sensor, int delay)
{
	event->type = PROTOCOL_CONTROL;
	event->packet.control.cmd = CONTROL_CMD_SENSOR;
	event->packet.control.direct = DIRECT_FROM_SERVER;
	event->packet.control.argv.b32[0] = 2;
	event->packet.control.argv.b32[1] = sensor;
	event->packet.control.argv.b32[2] = delay;
}

void data_set_test(struct protocol_handle *handle, struct protocol_event *event, char *test)
{
	event->type = PROTOCOL_TEST;
	strncpy(event->packet.test, test, 30);
}

void data_set_sensor_data(struct protocol_handle *handle, struct protocol_event *event, int num, struct amt_sensor_data *data)
{
	int i;
	memset(event, 0, sizeof(struct protocol_event));
	event->type = PROTOCOL_SENSOR;
	for(i = 0; i < num; i++)
	{
		event->packet.sensor[i].sensor_type = data[i].sensor_type;
		event->packet.sensor[i].data[0] = data[i].data[0];
		event->packet.sensor[i].data[1] = data[i].data[1];
		event->packet.sensor[i].data[2] = data[i].data[2];
	}
}

static int recv_command(struct protocol_handle *handle, struct control_data *cmd)
{
	int ret = 0;
	switch(cmd->cmd)
	{
		case CONTROL_CMD_UDP_PORT:
			if(cmd->direct == DIRECT_FROM_SERVER)
			{
				int port = cmd->argv.b16[0];
				if(handle->update_udp_port)
					handle->update_udp_port(handle->data, port);
			}
			break;

		case CONTROL_CMD_SENSOR:
			if(cmd->direct == DIRECT_FROM_SERVER)
			{
				if(cmd->argv.b32[0] == 1)
				{
					int sensor = cmd->argv.b32[1];
					int on = cmd->argv.b32[2];
					if(handle->sensor_control)
						handle->sensor_control(handle->data, sensor, on);
				}
				else if(cmd->argv.b32[0] == 2)
				{
					int sensor = cmd->argv.b32[1];
					int delay = cmd->argv.b32[2];
					if(handle->sensor_delay)
						handle->sensor_delay(handle->data, sensor, delay);
				}
			}
			break;

		case CONTROL_CMD_LOCAION:
			break;

		case CONTROL_CMD_KEY:
			break;

		case CONTROL_CMD_MOUSE:
			break;

		case CONTROL_CMD_TOUCH:
			break;

		default:
			ret = -1;
			break;
	}
	return ret;
}

int recv_packet(struct protocol_handle *handle, struct protocol_event *event)
{
	int ret = 0;
	switch(event->type)
	{
		case PROTOCOL_CONTROL:
			ret = recv_command(handle, &event->packet.control);
			break;

		case PROTOCOL_TOUCH:
			break;

		case PROTOCOL_KEY:
			break;

		case PROTOCOL_MOUSE:
			break;

		case PROTOCOL_LOCATION:
			break;

		case PROTOCOL_TEST:
			if(handle->update_test)
				handle->update_test(handle->data, event->packet.test);
			break;

		case PROTOCOL_SENSOR:
			{
				int num = 0;
				struct amt_sensor_data data[MAX_SENSOR_TYPE];
				while(event->packet.sensor[num].sensor_type)
				{
					data[num].sensor_type = event->packet.sensor[num].sensor_type;
					data[num].data[0] = event->packet.sensor[num].data[0];
					num++;
				}
				if(handle->sensor_data)
					handle->sensor_data(handle->data, num, data);
			}
			break;

		default:
			ret = -1;
			break;
	}
	return ret;
}

