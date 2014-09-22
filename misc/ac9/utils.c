#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
unsigned long timestamp()
{
	struct timeval time;
	unsigned long timestamp;
	gettimeofday(&time, NULL);
	timestamp = (unsigned long)time.tv_sec * 1000LL + time.tv_usec / 1000;
	return timestamp;
}

