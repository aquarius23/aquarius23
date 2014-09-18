#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jpeglib.h>

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

int decompress_jpeg(const char *jpeg_file, unsigned char *rgb, int *size)
{
	struct jpeg_decompress_struct cinfo;
	struct jpeg_error_mgr jerr;
	FILE *input_file;
	JSAMPARRAY buffer;
	int row_width;

	*size = 0;
	cinfo.err = jpeg_std_error(&jerr);
	jpeg_create_decompress(&cinfo);
	if((input_file = fopen(jpeg_file, "rb")) == NULL)
		return -1;
	jpeg_stdio_src(&cinfo, input_file);
	jpeg_read_header(&cinfo, TRUE);
	cinfo.out_color_space = JCS_EXT_RGB;
	jpeg_start_decompress(&cinfo);
	row_width = cinfo.output_width * cinfo.output_components;
	buffer = (*cinfo.mem->alloc_sarray)((j_common_ptr)&cinfo, JPOOL_IMAGE, row_width, 1);
	printf("width:height:component = %d:%d:%d\n", cinfo.output_width, cinfo.output_height, cinfo.out_color_components);
	while(cinfo.output_scanline < cinfo.output_height)
	{
		jpeg_read_scanlines(&cinfo, buffer, 1);
		memcpy(rgb, *buffer, row_width);
		rgb += row_width;
		*size += row_width;
	}
	jpeg_finish_decompress(&cinfo);
	jpeg_destroy_decompress(&cinfo);
	fclose(input_file);
	return 0;
}

int main(void)
{
	int size;
	decompress_jpeg("1.jpeg", rgb, &size);
	printf("rgb size = %d\n", size);
	save_buffer("1.rgb", rgb, size);
	return 0;
}

