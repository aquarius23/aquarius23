#include <stdio.h>
#include <stdlib.h>
#include "yuv2rgb.h"
#include "jpeg.h"

#define MAX_HEIGHT 8000
#define MAX_WIDTH 8000
#define HEIGHT 3120
#define WIDTH 4160
void save_buffer(const char *file, void *buf, int size)
{
	FILE *p = fopen(file, "wb+");
	if(p > 0)
	{
		fwrite(buf, size, 1, p);
		fclose(p);
	}
}

void read_buffer(const char *file, void *buf, int size)
{
	FILE *p = fopen(file, "rb");
	if(p > 0)
	{
		fread(buf, size, 1, p);
		fclose(p);
	}
}

unsigned char yuv[MAX_HEIGHT*MAX_WIDTH*3/2];
unsigned char rgb[MAX_HEIGHT*MAX_WIDTH*3];

int main(void)
{
	read_buffer("1.yuv", yuv, HEIGHT*WIDTH*3/2);
	yuv2rgb_semi(yuv, (unsigned short *)yuv + WIDTH*HEIGHT, rgb, WIDTH, HEIGHT);
	compress_jpeg_rgb888(rgb, WIDTH, HEIGHT, "1.jpeg");
}
