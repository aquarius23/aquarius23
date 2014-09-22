#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jpeglib.h>
#include <libexif/exif-data.h>

struct exif_iso_shutter
{
	int iso;
	int shutter;
	int width;
	int height;
	void *ifd;
};

static void read_exif_entry(ExifEntry *ee, void *user_data)
{
	int one;
	char v[1024];
	struct exif_iso_shutter *exif = (struct exif_iso_shutter*)user_data;
	const char *title = exif_tag_get_title_in_ifd(ee->tag, *((ExifIfd*)exif->ifd));
	const char *value = exif_entry_get_value(ee, v, sizeof(v));
	if(strcmp("Exposure Time", title) == 0)
		sscanf(value, "%d/%d", &one, &exif->shutter);
	else if(strcmp("ISO Speed Ratings", title) == 0)
		sscanf(value, "%d", &exif->iso);
	else if(strcmp("Pixel X Dimension", title) == 0)
		sscanf(value, "%d", &exif->width);
	else if(strcmp("Pixel Y Dimension", title) == 0)
		sscanf(value, "%d", &exif->height);
	//printf("%s: %s\n", title, value);
}

static void read_exif_content(ExifContent *ec, void *user_data)
{
	ExifIfd ifd = exif_content_get_ifd(ec);
	struct exif_iso_shutter *exif = (struct exif_iso_shutter *)user_data;
	exif->ifd = (void *)&ifd;
	exif_content_foreach_entry(ec, read_exif_entry, exif);
}

int read_exif(const char *file_name, int *shutter, int *iso, int *width, int *height)
{
	struct exif_iso_shutter exif;
	ExifData* ed = exif_data_new_from_file(file_name);
	if(!ed)
		return -1;
	exif_data_foreach_content(ed, read_exif_content, &exif);
	exif_data_unref(ed);
	if(shutter)
		*shutter = exif.shutter;
	if(iso)
		*iso = exif.iso;
	if(width)
		*width = exif.width;
	if(height)
		*height = exif.height;
	return 0;
}

int decompress_jpeg(const char *jpeg_file, unsigned char *rgb, int *size, int *width, int *height)
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
	if(width)
		*width = cinfo.output_width;
	if(height)
		*height = cinfo.output_height;
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

