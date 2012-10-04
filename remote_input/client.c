#include "log.h"
#include "communicator.h"
#include "protocol.h"

static struct amt_event_base *g_base;
static SOCKET g_tcp, g_udp;
static struct sockaddr g_udp_addr;

static void event_read_cb(void *arg)
{
	int size;
	struct sockaddr addr;
	struct protocol_event packet;
	struct amt_event *event = arg;
	size = amt_event_buffer_read(event, &packet, sizeof(struct protocol_event), &addr);
	LOGD("%s read test = %s\n", __func__, packet.packet.test);
}

int init_client_sock(void)
{
	g_udp = create_udp_sock();
	g_base = amt_event_base_init();
	amt_event_base_loop(g_base);
	return 0;
}

static void test_send(struct amt_event *event)
{
	struct protocol_event packet;
	while(1)
	{
		static int iterator = 0;
		sprintf(packet.packet.test, "%d 123456789asdfghh", iterator++);
		amt_event_buffer_write(event, &packet, sizeof(struct protocol_event), NULL);
		usleep(200000);
	}
}

int connect_server(char *ip, int port)
{
	struct amt_event *event;
	g_tcp = connect_tcp_addr(ip, port);
	if(g_tcp < 0)
	{
		LOGE("%s error\n", __func__);
		return -1;
	}
	amt_set_sockaddr(&g_udp_addr, ip, port);
	event = amt_event_set(g_base, g_tcp, TYPE_TCP);
	amt_event_add(g_base, event, event_read_cb, event);
	test_send(event);
	return 0;
}

