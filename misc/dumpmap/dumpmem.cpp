#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <utils/Log.h>

#define DUMP_PID 825
#define DUMP_ADDRESS 0xdb714000
#define DUMP_SIZE 0x1000
#define DUMP_FILE "/data/misc/camera/mem.bin"

void dump(int dst, int src, int size)
{
	char buf[1024];
	while (size) {
		int read_size = size;
		if (read_size > 1024)
			read_size = 1024;
		read(src, buf, read_size);
		write(dst, buf, read_size);
		size -= read_size;
	}
}

void dump_mem(int pid, long addr, int size, const char *file)
{
	char path[256];
	snprintf(path, 256, "/proc/%d/mem", pid);
	int src = open(path, O_RDONLY);
	int dst = open(file, O_WRONLY | O_CREAT | O_TRUNC);
	if (src > 0 && dst > 0) {
		lseek64(src, addr, SEEK_SET);
		dump(dst, src, size);
	}
	if (src > 0)
		close(src);
	if (dst > 0)
		close(dst);
}

int main(void)
{
	dump_mem(DUMP_PID, DUMP_ADDRESS, DUMP_SIZE, (const char *)DUMP_FILE);
	return 0;
}
