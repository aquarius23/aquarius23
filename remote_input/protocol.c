#include "protocol.h"

void cmd_set_udp_port(struct protocol_event *event, unsigned short port)
{
	event->type = PROTOCOL_CONTROL;
	event->packet.control.cmd = CONTROL_CMD_UDP_PORT;
	event->packet.control.argv.b16[0] = port;
}

static int recv_command(struct control_data *cmd)
{
	int ret = 0;
	switch(cmd->cmd)
	{
		case CONTROL_CMD_UDP_PORT:
			if(cmd->direct == DIRECT_FROM_SERVER)
			{
				int port = cmd->argv.b16[0];
				//TODO
			}
			break;

		case CONTROL_CMD_SENSOR:
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

int recv_packet(struct protocol_event *event)
{
	int ret = 0;
	switch(event->type)
	{
		case PROTOCOL_CONTROL:
			ret = recv_command(&event->packet.control);			
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
			break;

		default:
			ret = -1;
			break;
	}
	return ret;
}

