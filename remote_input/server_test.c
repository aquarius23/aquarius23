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

void mouse_data(int x, int y, int button, int press)
{
	printf("%s x = %d y = %d button = %d press = %d\n", __func__, x, y, button, press);
}

void touch_data(int num, int *x, int *y, int *press)
{
	printf("%s num = %d x = %d y = %d press = %d\n", __func__, num, *x, *y, *press);
}

void key_data(int code, int press)
{
	printf("%s code = %d press = %d\n", __func__, code, press);
}

#ifdef WIN32
void update_sensor(float g_sensor_y, float o_sensor_x, float cal);
void win32_sensor(int num, struct amt_sensor_data *sensor)
{
	int i;
	static float last_x = 0, last_y = 0;
	int vx = 0, vy = 0;
	for(i = 0; i < num; i++)
	{
		if(sensor[i].sensor_type == 1)
		{
			vy = 1;
			last_y = sensor[i].data[1];
		}
		if(sensor[i].sensor_type == 3)
		{
			vx = 1;
			last_x = sensor[i].data[0];
		}
	}
	if(vx || vy)
		update_sensor(last_x, last_y, 16);
}
#endif

void sensor_data(int num, struct amt_sensor_data *sensor)
{
#ifdef WIN32
	win32_sensor(num, sensor);
#endif
//	while(num--)
//		printf("sensor type = %d, x = %f, y = %f, z = %f\n", sensor[num].sensor_type, sensor[num].data[0], sensor[num].data[1], sensor[num].data[2]);
}

int main(void)
{
	struct amt_handle *handle;
	struct amt_server_callback cb;
	memset(&cb, 0, sizeof(struct amt_server_callback));
	cb.log_cb = log_cb;
	cb.update_test = update_test;
	cb.sensor_data = sensor_data;
	cb.mouse_data = mouse_data;
	cb.touch_data = touch_data;
	cb.key_data = key_data;
	handle = init_server_sock(&cb);
	control_server_log(handle, CB_LOGA);
	while(1)
	{
		int ret = sensor_server_control(handle, 1, 1);
		sensor_server_control(handle, 3, 1);
		if(ret == RETURN_NORMAL)
			break;
		usleep(900000);
	}
	while(1)
		usleep(900000);
	return 0;
}

