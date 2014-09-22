#ifndef _JPEG_H
#define _JPEG_H
int read_exif(const char *file_name, int *shutter, int *iso, int *width, int *height);
int decompress_jpeg(const char *jpeg_file, unsigned char *rgb, int *size, int *width, int *height);
int compress_jpeg_rgb888(const unsigned char *rgb, int width, int height, const char *jpeg_file);
#endif
