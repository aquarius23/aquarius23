#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jpeglib.h>
#include <libexif/exif-data.h>

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

void read_exif_entry(ExifEntry *ee, void* ifd)
{
	char v[1024];
	printf("%s: %s\n"
		,exif_tag_get_title_in_ifd(ee->tag, *((ExifIfd*)ifd))
		,exif_entry_get_value(ee, v, sizeof(v)));
}

void read_exif_content(ExifContent *ec, void *user_data)
{
	ExifIfd ifd = exif_content_get_ifd(ec);
	exif_content_foreach_entry(ec, read_exif_entry, &ifd);
}

int read_exif(char *file_name)
{
	ExifData* ed = exif_data_new_from_file(file_name);
	if(!ed)
		return -1;
	exif_data_foreach_content(ed, read_exif_content, NULL);
	exif_data_unref(ed);
	return 0;
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

int compress_jpeg_rgb888(const unsigned char *rgb, int width, int height, const char *jpeg_file)
{
	FILE *out_file;
	struct jpeg_compress_struct cinfo;
	struct jpeg_error_mgr jerr;
	JSAMPROW row_pointer[1];
	int row_width;

	cinfo.err = jpeg_std_error(&jerr);
	jpeg_create_compress(&cinfo);
	if((out_file = fopen(jpeg_file, "wb+")) == NULL)
		return -1;
	jpeg_stdio_dest(&cinfo, out_file);
	cinfo.image_width = width;
	cinfo.image_height = height;
	cinfo.input_components = 3;
	cinfo.in_color_space = JCS_EXT_RGB;
	jpeg_set_defaults(&cinfo);
	jpeg_set_quality(&cinfo, 95, TRUE);
	jpeg_start_compress(&cinfo, TRUE);

	row_width = cinfo.image_width * cinfo.input_components;
	while (cinfo.next_scanline < cinfo.image_height) {
		row_pointer[0] = (JSAMPROW)&rgb[cinfo.next_scanline * row_width];
		jpeg_write_scanlines(&cinfo, row_pointer, 1);
	}
	jpeg_finish_compress(&cinfo);
	jpeg_destroy_compress(&cinfo);
	fclose(out_file);
	return 0;
}

int main(void)
{
	int size;
	decompress_jpeg("1.jpeg", rgb, &size);
	printf("rgb size = %d\n", size);
	compress_jpeg_rgb888(rgb, 3264, 2448, "2.jpeg");
	read_exif("1.jpeg");
	save_buffer("1.rgb", rgb, size);
	return 0;
}

