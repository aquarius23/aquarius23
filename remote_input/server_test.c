#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "amt_remote.h"
#include "log.h"

void log_cb(int tag, const char *log)
{
	printf("%s", log);
}

int main(void)
{
	amt_log_register(log_cb);
	amt_log_control(CB_LOGA);
	init_server_sock(NULL);
	while(1)
		usleep(100000);
	return 0;
}

