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
	struct amt_event *event_tcp, *event_udp;
	struct sockaddr sock_udp_addr;
	struct amt_client_callback cb;
	struct amt_log_handle log_handle;
	struct protocol_handle protocol;
};

static void event_read_cb(void *arg)
{
	int size;
	struct sockaddr addr;
	struct protocol_event packet;
	struct amt_event *event = arg;
	struct amt_client *client = (struct amt_client*)event->base;
	size = amt_event_buffer_read(event, &packet, sizeof(struct protocol_event), &addr);
	if(size <= 0)
	{
		LOGE(&client->log_handle, "%s socket error\n", __func__);
		close_socket(event->sock);
		amt_event_del_safe(event);
	}
	else
		size = recv_packet(&client->protocol, &packet);
	if(size == 2)
		amt_event_buffer_write(event, &packet, sizeof(struct protocol_event), NULL);
}

static int __update_udp_port(void *arg, unsigned short port)
{
	struct amt_client *client = arg;
	LOGD(&client->log_handle, "%s: %d\n", __func__, port);
	return RETURN_NORMAL;
}

static int __sensor_control(void *arg, int sensor, int on)
{
	int ret = RETURN_ERROR;
	struct amt_client *client = arg;
	LOGD(&client->log_handle, "%s: sensor = %d, on = %d\n", __func__, sensor, on);
	if(client->cb.sensor_control)
		ret = client->cb.sensor_control(sensor, on);
	return ret;
}

static int __sensor_delay(void *arg, int sensor, int delay)
{
	int ret = RETURN_NORMAL;
	struct amt_client *client = arg;
	LOGD(&client->log_handle, "%s: sensor = %d, delay = %d\n", __func__, sensor, delay);
	if(client->cb.sensor_delay)
		ret = client->cb.sensor_delay(sensor, delay);
	return ret;
}

static void init_protocol(struct amt_client *client)
{
	client->protocol.data = client;
	client->protocol.log = &client->log_handle;
	client->protocol.update_udp_port = __update_udp_port;
	client->protocol.sensor_control = __sensor_control;
	client->protocol.sensor_delay = __sensor_delay;
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
	{
		memcpy(&a_client->cb, cb, sizeof(struct amt_client_callback));
		if(cb->log_cb)
			amt_log_register(&a_client->log_handle, cb->log_cb);
	}
	init_protocol(a_client);
	amt_event_base_loop(a_client->event_base);
	a_handle->type = AMT_CLIENT;
	a_handle->point = a_client;
	return a_handle;
}

int connect_client2server(struct amt_handle *handle, char *ip, int port)
{
	struct amt_event *event;
	struct amt_client *client;
	if(handle->type != AMT_CLIENT)
		return -1;
	client = handle->point;
	client->sock_tcp = connect_tcp_addr(ip, port);
	if(client->sock_tcp < 0)
	{
		LOGE(&client->log_handle, "%s error\n", __func__);
		return -1;
	}
	amt_set_sockaddr(&client->sock_udp_addr, ip, port);
	event = amt_event_set(&client->event_base, client->sock_tcp, TYPE_TCP);
	amt_event_add(client->event_base, event, event_read_cb, event);
	client->event_tcp = event;
	return 0;
}

void control_client_log(struct amt_handle *handle, int tag_on)
{
	struct amt_client *client;
	if(handle->type != AMT_CLIENT)
		return;
	client = handle->point;
	if(client->cb.log_cb)
		amt_log_control(&client->log_handle, tag_on);
}

void data_client_send_test(struct amt_handle *handle, char *test)
{
	struct protocol_event packet;
	struct amt_client *client;
	if(handle->type != AMT_CLIENT)
		return;
	client = handle->point;
	data_set_test(&client->protocol, &packet, test);
	amt_event_buffer_write_sync(client->event_tcp, &packet, sizeof(struct protocol_event), NULL);
}

void sensor_client_send_data(struct amt_handle *handle, int num, struct amt_sensor_data *sensor)
{
	struct protocol_event packet;
	struct amt_client *client;
	if(handle->type != AMT_CLIENT)
		return;
	client = handle->point;
	data_set_sensor_data(&client->protocol, &packet, num, sensor);
	amt_event_buffer_write_sync(client->event_tcp, &packet, sizeof(struct protocol_event), NULL);
}

