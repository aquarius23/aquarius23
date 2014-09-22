#include <stdio.h>
#include <stdlib.h>
#include "jpeg.h"

unsigned char rgb[3264*2448*3];
void save_buffer(const char *file, void *buf, int size)
{
	FILE *p = fopen(file, "wb+");
	if(p > 0)
	{
		fwrite(buf, size, 1, p);
		fclose(p);
	}
}

int main(int argc,char *argv[])
{
	char *cmd, *name;
	int size, shutter, iso, width, height;
	cmd = NULL;
	if(argc >= 3)
	{
		cmd = argv[1];
		name = argv[2];
		printf("cmd: %s\n", cmd);
	}
	else
	{
		printf("cmd file-prefix\ncmd:\n     lowlight\n     hdr\n");
	}
	decompress_jpeg("1.jpeg", rgb, &size, &width, &height);
	printf("rgb size = %d width:height = %d:%d\n", size, width, height);
	compress_jpeg_rgb888(rgb, 3264, 2448, "2.jpeg");
	read_exif("1.jpeg", &shutter, &iso, &width, &height);
	save_buffer("1.rgb", rgb, size);
	printf("shutter:iso = 1/%d sec:%d\n", shutter, iso);
	return 0;
}

