#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "amt_remote.h"
#include "log.h"

void log_cb(int tag, const char *log)
{
	printf("%s", log);
}

void update_test(char *test)
{
	printf("%s\n", test);
}

int main(void)
{
	struct amt_handle *handle;
	struct amt_server_callback cb;
	cb.log_cb = log_cb;
	cb.update_test = update_test;
	handle = init_server_sock(&cb);
	control_server_log(handle, CB_LOGA);
	while(1)
		usleep(100000);
	return 0;
}

