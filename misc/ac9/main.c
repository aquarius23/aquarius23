#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "jpeg.h"
#include "merge.h"

void save_buffer(const char *file, void *buf, int size)
{
	FILE *p = fopen(file, "wb+");
	if(p > 0)
	{
		fwrite(buf, size, 1, p);
		fclose(p);
	}
}

static char iterator_name[128];
char *get_iterator_name(char *prefix, int index)
{
	sprintf(iterator_name, "%s-%d.jpg", prefix, index);
	return iterator_name;
}

int main(int argc,char *argv[])
{
	int i;
	char *cmd, *name;
	int size, shutter, iso, width, height;
	cmd = NULL;
	if(argc >= 3)
	{
		cmd = argv[1];
		name = argv[2];
		printf("cmd: %s\n", cmd);
		if(strcmp("lowlight", cmd) == 0)
		{
			unsigned char *in[4];
			unsigned char *out;
			char *file;
			file = get_iterator_name(name, 0);
			read_exif(file, &shutter, &iso, &width, &height);
			printf("iso:shutter = %d:%d width:height = %d:%d\n", iso, shutter, width, height);
			for(i = 0; i < 4; i++)
			{
				in[i] = (unsigned char *)malloc(width * height * 3);
			}
			out = (unsigned char *)malloc(width * height * 3);
			for(i = 0; i < 4; i++)
			{
				file = get_iterator_name(name, i);
				decompress_jpeg(file, in[i], &size, &width, &height);
			}
			shlaLowLight(in, out, &width, &height);
			compress_jpeg_rgb888(out, width, height, "lowlight.jpeg");
			for(i = 0; i < 4; i++)
				free(in[i]);
			free(out);
		}
		else if(strcmp("hdr", cmd) == 0)
		{
			unsigned char *in[3];
			unsigned char *out;
			char *file;
			file = get_iterator_name(name, 0);
			read_exif(file, &shutter, &iso, &width, &height);
			printf("iso:shutter = %d:%d width:height = %d:%d\n", iso, shutter, width, height);
			for(i = 0; i < 3; i++)
			{
				in[i] = (unsigned char *)malloc(width * height * 3);
			}
			out = (unsigned char *)malloc(width * height * 3);
			for(i = 0; i < 4; i++)
			{
				file = get_iterator_name(name, i);
				decompress_jpeg(file, in[i], &size, &width, &height);
			}
			shlaHDR(in, out, &width, &height);
			compress_jpeg_rgb888(out, width, height, "hdr.jpeg");
			for(i = 0; i < 3; i++)
				free(in[i]);
			free(out);
		}
		else if(strcmp("autofix", cmd) == 0)
		{
			unsigned char *in, *out;
			read_exif(name, &shutter, &iso, &width, &height);
			printf("iso:shutter = %d:%d width:height = %d:%d\n", iso, shutter, width, height);
			in = (unsigned char *)malloc(width * height * 3);
			out = (unsigned char *)malloc(width * height * 3);
			decompress_jpeg(name, in, &size, &width, &height);
			shlaAutoFix(in, out, width, height);
			compress_jpeg_rgb888(out, width, height, "autofix.jpeg");
			free(in);
			free(out);
		}
	}
	else
	{
		printf("cmd file-prefix\ncmd:\n     lowlight\n     hdr\n     autofix\n");
	}
	return 0;
}

