#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "amt_remote.h"

void log_cb(int tag, const char *log)
{
	printf("%s", log);
}

void update_test(char *test)
{
	printf("%s\n", test);
}

void sensor_data(int num, struct amt_sensor_data *sensor)
{
	while(num--)
		printf("sensor type = %d, x = %f, y = %f, z = %f\n", sensor[num].sensor_type, sensor[num].data[0], sensor[num].data[1], sensor[num].data[2]);
}

int main(void)
{
	struct amt_handle *handle;
	struct amt_server_callback cb;
	memset(&cb, 0, sizeof(struct amt_server_callback));
	cb.log_cb = log_cb;
	cb.update_test = update_test;
	cb.sensor_data = sensor_data;
	handle = init_server_sock(&cb);
	control_server_log(handle, CB_LOGA);
	while(1)
	{
		int ret = sensor_server_control(handle, 1, 1);
		sensor_server_control(handle, 2, 1);
		sensor_server_control(handle, 3, 1);
		if(ret == RETURN_NORMAL)
			break;
		usleep(2000000);
	}
	while(1)
		usleep(100000);
	return 0;
}

