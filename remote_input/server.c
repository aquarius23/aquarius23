#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "log.h"
#include "communicator.h"
#include "protocol.h"

struct amt_server
{
	struct amt_event_base *event_base;
	SOCKET sock_tcp, sock_udp;
	unsigned short tcp_port, udp_port;
	struct amt_server_callback cb;
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

static void event_listen_cb(void *arg)
{
	struct sockaddr addr;
	SOCKET new_sock;
	struct amt_event *new_event;
	struct amt_event *event = arg;
	new_sock = amt_sock_accept(event->sock, &addr);
	LOGD("%s accept ip: %s\n", __func__, amt_get_ip(&addr));
	new_event = amt_event_set(event->base, new_sock, TYPE_TCP);
	amt_event_add(event->base, new_event, event_read_cb, new_event);
}

struct amt_handle *init_server_sock(struct amt_server_callback *cb)
{
	struct amt_event *event;
	int port = SERVER_PORT;
	struct amt_server *a_server;
	struct amt_handle *a_handle;

	a_handle= malloc(sizeof(struct amt_handle));
	if(!a_handle)
		return NULL;
	a_server = malloc(sizeof(struct amt_server));
	memset(a_server, 0, sizeof(struct amt_server));
	if(!a_server)
	{
		free(a_handle);
		return NULL;
	}

	communicator_init();
	a_server->event_base = amt_event_base_init();
	do
	{
		a_server->sock_tcp = listen_tcp_port(port);
		if(a_server->sock_tcp > 0)
		{
			LOGD("%s open tcp port = %d\n", __func__, port);
			break;
		}
		else
			LOGD("%s can't open tcp port = %d", __func__, port);
	} while(++port);
	a_server->tcp_port = port;
	event = amt_event_set(a_server->event_base, a_server->sock_tcp, TYPE_TCP);
	amt_event_add(a_server->event_base, event, event_listen_cb, event);
	
	while(++port)
	{
		a_server->sock_udp = listen_udp_port(port);
		if(a_server->sock_udp > 0)
		{
			LOGD("%s open udp port = %d\n", __func__, port);
			break;
		}
		else
			LOGD("%s can't open udp port = %d", __func__, port);
	}
	a_server->udp_port = port;
	event = amt_event_set(a_server->event_base, a_server->sock_udp, TYPE_UDP);
	amt_event_add(a_server->event_base, event, event_listen_cb, event);

	if(cb)
		memcpy(&a_server->cb, cb, sizeof(struct amt_server_callback));
	amt_event_base_loop(a_server->event_base);
	a_handle->type = AMT_SERVER;
	a_handle->point = a_server;

	return a_handle;
}

