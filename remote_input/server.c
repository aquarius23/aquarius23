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
	struct amt_log_handle log_handle;
	struct protocol_handle protocol;
};

static void event_read_cb(void *arg)
{
	int size;
	struct sockaddr addr;
	struct protocol_event packet;
	struct amt_event *event = arg;
	struct amt_server *server = (struct amt_server *)event->base;
	size = amt_event_buffer_read(event, &packet, sizeof(struct protocol_event), &addr);
	if(size <= 0)
	{
		LOGE(&server->log_handle, "%s socket error\n", __func__);
		close_socket(event->sock);
		amt_event_del_safe(event);
	}
	else
		recv_packet(&server->protocol, &packet);
}

static void event_listen_cb(void *arg)
{
	struct sockaddr addr;
	SOCKET new_sock;
	struct protocol_event packet;
	struct amt_event *new_event;
	struct amt_event *event = arg;
	struct amt_server *server = (struct amt_server *)event->base;
	new_sock = amt_sock_accept(event->sock, &addr);
	LOGD(&server->log_handle, "%s accept ip: %s\n", __func__, amt_get_ip(&addr));
	new_event = amt_event_set(event->base, new_sock, TYPE_TCP);
	amt_event_add(*event->base, new_event, event_read_cb, new_event);

	cmd_set_udp_port(&server->protocol, &packet, server->udp_port);
	amt_event_buffer_write(new_event, &packet, sizeof(struct protocol_event), NULL);
}

static void update_test(void *arg, char *test)
{
	struct amt_server *server = arg;
	if(server->cb.update_test)
		server->cb.update_test(test);
}

static void init_protocol(struct amt_server *server)
{
	server->protocol.data = server;
	server->protocol.log = &server->log_handle;
	server->protocol.update_test = update_test;
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

	if(cb)
	{
		memcpy(&a_server->cb, cb, sizeof(struct amt_server_callback));
		if(cb->log_cb)
			amt_log_register(&a_server->log_handle, cb->log_cb);
	}

	if(a_server->cb.log_cb)
		amt_log_control(&a_server->log_handle, CB_LOGA); //enable init log

	init_protocol(a_server);
	communicator_init();
	a_server->event_base = amt_event_base_init();
	do
	{
		a_server->sock_tcp = listen_tcp_port(port);
		if(a_server->sock_tcp > 0)
		{
			LOGD(&a_server->log_handle, "%s open tcp port = %d\n", __func__, port);
			break;
		}
		else
			LOGD(&a_server->log_handle, "%s can't open tcp port = %d\n", __func__, port);
	} while(++port);
	a_server->tcp_port = port;
	event = amt_event_set(&a_server->event_base, a_server->sock_tcp, TYPE_TCP);
	amt_event_add(a_server->event_base, event, event_listen_cb, event);
	
	while(++port)
	{
		a_server->sock_udp = listen_udp_port(port);
		if(a_server->sock_udp > 0)
		{
			LOGD(&a_server->log_handle, "%s open udp port = %d\n", __func__, port);
			break;
		}
		else
			LOGD(&a_server->log_handle, "%s can't open udp port = %d", __func__, port);
	}
	a_server->udp_port = port;
	event = amt_event_set(&a_server->event_base, a_server->sock_udp, TYPE_UDP);
	amt_event_add(a_server->event_base, event, event_listen_cb, event);

	amt_event_base_loop(a_server->event_base);
	a_handle->type = AMT_SERVER;
	a_handle->point = a_server;

	if(a_server->cb.log_cb)
		amt_log_control(&a_server->log_handle, CB_LOGA); //disable init log

	return a_handle;
}

void control_server_log(struct amt_handle *handle, int tag_on)
{
	struct amt_server *server;
	if(handle->type != AMT_SERVER)
		return;
	server = handle->point;
	if(server->cb.log_cb)
		amt_log_control(&server->log_handle, tag_on);
}

