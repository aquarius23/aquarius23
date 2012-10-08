#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "amt_remote.h"
#include "log.h"

void log_cb(int tag, const char *log)
{
	printf("%s\n", log);
}

int main(void)
{
	struct amt_handle *handle;
	amt_log_register(log_cb);
	amt_log_control(CB_LOGA);
	handle = init_client_sock(NULL);
	connect_server(handle, "127.0.0.1", SERVER_PORT);
	while(1)
		usleep(100000);
	return 0;
}

