#include "log.h"
#include "communicator.h"
#include "protocol.h"

static struct amt_event_base *g_base;
static SOCKET g_tcp, g_udp;

static void event_read_cb(void *arg)
{
	int size;
	struct sockaddr addr;
	struct protocol_event packet;
	struct amt_event *event = arg;
	size = amt_event_buffer_read(event, &packet, sizeof(struct protocol_event), &addr);
	LOGD("%s read test = %s\n", __func__, packet.packet.test);
}

static void event_listen_cb(void *arg)
{
	struct sockaddr addr;
	SOCKET new_sock;
	struct amt_event *new_event;
	struct amt_event *event = arg;
	new_sock = amt_sock_accept(event->sock, &addr);
	LOGD("%s accept ip: %s\n", __func__, amt_get_ip(&addr));
	new_event = amt_event_set(g_base, new_sock, TYPE_TCP);
	amt_event_add(g_base, new_event, event_read_cb, new_event);
}

int init_server_sock(void)
{
	struct amt_event *event;
	int port = SERVER_PORT;
	communicator_init();
	g_base = amt_event_base_init();
	do
	{
		g_tcp = listen_tcp_port(port);
		if(g_tcp > 0)
		{
			LOGD("%s open tcp port = %d\n", __func__, port);
			break;
		}
		else
			LOGD("%s can't open tcp port = %d", __func__, port);
	} while(++port);
	event = amt_event_set(g_base, g_tcp, TYPE_TCP);
	amt_event_add(g_base, event, event_listen_cb, event);
	
	while(++port)
	{
		g_udp = listen_udp_port(port);
		if(g_udp > 0)
		{
			LOGD("%s open udp port = %d\n", __func__, port);
			break;
		}
		else
			LOGD("%s can't open udp port = %d", __func__, port);
 
	}
	event = amt_event_set(g_base, g_udp, TYPE_UDP);
	amt_event_add(g_base, event, event_listen_cb, event);

	amt_event_base_loop(g_base);
	return 0;
}

