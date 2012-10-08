#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "log.h"
#include "communicator.h"
#include "protocol.h"

struct amt_client
{
	struct amt_event_base *event_base;
	SOCKET sock_tcp, sock_udp;
	struct sockaddr sock_udp_addr;
	struct amt_client_callback cb;
};

static void event_read_cb(void *arg)
{
	int size;
	struct sockaddr addr;
	struct protocol_event packet;
	struct amt_event *event = arg;
	size = amt_event_buffer_read(event, &packet, sizeof(struct protocol_event), &addr);
	if(size <= 0)
	{
		LOGE("%s socket error\n", __func__);
		close_socket(event->sock);
		amt_event_del_safe(event);
	}
	else
		LOGD("%s read test = %s\n", __func__, packet.packet.test);
}

struct amt_handle *init_client_sock(struct amt_client_callback *cb)
{
	struct amt_client *a_client;
	struct amt_handle *a_handle;

	a_handle= malloc(sizeof(struct amt_handle));
	if(!a_handle)
		return NULL;
	a_client = malloc(sizeof(struct amt_client));
	memset(a_client, 0, sizeof(struct amt_client));
	if(!a_client)
	{
		free(a_handle);
		return NULL;
	}

	communicator_init();
	a_client->sock_udp = create_udp_sock();
	a_client->event_base = amt_event_base_init();

	if(cb)
		memcpy(&a_client->cb, cb, sizeof(struct amt_client_callback));
	amt_event_base_loop(a_client->event_base);
	a_handle->type = AMT_CLIENT;
	a_handle->point = a_client;
	return a_handle;
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

int connect_server(struct amt_handle *handle, char *ip, int port)
{
	struct amt_event *event;
	struct amt_client *client;
	if(handle->type != AMT_CLIENT)
		return -1;
	client = handle->point;
	client->sock_tcp = connect_tcp_addr(ip, port);
	if(client->sock_tcp < 0)
	{
		LOGE("%s error\n", __func__);
		return -1;
	}
	amt_set_sockaddr(&client->sock_udp_addr, ip, port);
	event = amt_event_set(client->event_base, client->sock_tcp, TYPE_TCP);
	amt_event_add(client->event_base, event, event_read_cb, event);
	test_send(event);
	return 0;
}

