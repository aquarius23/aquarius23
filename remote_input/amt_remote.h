#ifndef _AMT_REMOTE_H
#define _AMT_REMOTE_H

#define SERVER_PORT 11220

#define CB_LOGV	(1 << 0)
#define CB_LOGD	(1 << 1)
#define CB_LOGE	(1 << 2)
#define CB_LOGW	(1 << 3)
#define CB_LOGI	(1 << 4)
#define CB_LOGA	(CB_LOGV | CB_LOGD | CB_LOGE | CB_LOGW | CB_LOGI)

typedef void (*amt_log_callback)(int tag, const char *log);

struct amt_sensor_data
{
	short sensor_type;
	float data[3];
};

struct amt_server_callback
{
	amt_log_callback log_cb;
	void (*update_test)(char *test);
	void (*sensor_data)(int num, struct amt_sensor_data *sensor);
};

struct amt_client_callback
{
	amt_log_callback log_cb;
	int (*sensor_control)(int sensor, int on);
	int (*sensor_delay)(int sensor, int delay);
};

#define AMT_SERVER	1
#define AMT_CLIENT	2

#define RETURN_NORMAL   0
#define RETURN_ERROR    -1

struct amt_handle
{
	int type;
	void *point;
};

//server mode api
struct amt_handle *init_server_sock(struct amt_server_callback *cb);
void control_server_log(struct amt_handle *handle, int tag_on);
int sensor_server_control(struct amt_handle *handle, int sensor, int on);
int sensor_server_delay(struct amt_handle *handle, int sensor, int delay);
//client mode api
struct amt_handle *init_client_sock(struct amt_client_callback *cb);
int connect_client2server(struct amt_handle *handle, char *ip, int port);
void control_client_log(struct amt_handle *handle, int tag_on);
void data_client_send_test(struct amt_handle *handle, char *test);
void sensor_client_send_data(struct amt_handle *handle, int num, struct amt_sensor_data *sensor);
#endif

