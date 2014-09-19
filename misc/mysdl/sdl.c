#include <stdio.h>
#include <stdlib.h>
#include "SDL/SDL.h"

#define WIDTH 864
#define HEIGHT 480
#define MAX_FILE 32000000

unsigned char rgb8888[3264*2448*4];
unsigned char rgb_s[864*480*4];
void rgb_scale(char *dst, char *src, unsigned int dst_width, unsigned
		int dst_height, unsigned int src_width, unsigned int src_height)
{
    unsigned int x, y;
    unsigned int x_float_16 = (src_width << 16) / dst_width + 1;
    unsigned int y_float_16 = (src_height << 16) / dst_height + 1;
    unsigned int srcy_16 = 0;
    unsigned int src_width_adjust = src_width << 2;
    for(y = 0; y < dst_height; y++)
    {
        char *psrc_line = src + src_width_adjust * (srcy_16 >> 16);
        unsigned int srcx_16 = 0;
        for(x = 0; x < dst_width; x++)
        {
            int index = y * dst_width + x;
            ((int *)dst)[index] = ((int *)psrc_line)[srcx_16 >> 16];
            srcx_16 += x_float_16;
        }
        srcy_16 += y_float_16;
    }
}

int Init()
{
	if(SDL_Init(SDL_INIT_VIDEO) == -1)
	{
		fprintf(stderr,"SDL init error:%s",SDL_GetError());
		return -1;
	}
	return 0;
}

SDL_Surface *create_surface(int width, int height)
{
	return SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0, 0, 0, 0);
}

SDL_Surface *createScreen(int width , int height , int bpp , Uint32 flags)
{
	SDL_Surface *screen;
	screen = SDL_SetVideoMode(width, height, bpp, flags);
	if(screen == NULL)
	{
		printf("Could not Creat a Screen!:%s",SDL_GetError());
		return 0;
	}
	return screen;
}

static unsigned char g_file_buffer[MAX_FILE];
unsigned char *read_file(char *file)
{
	FILE *p = fopen(file, "rb+");
	if(p > 0)
	{
		int size;
		fseek(p, 0, SEEK_END);
		size = ftell(p);
		fseek(p, 0, SEEK_SET);
		fread(g_file_buffer, size, 1, p);
		fclose(p);
		return g_file_buffer;
	}
	return NULL;
}

void test_draw(SDL_Surface *surface)
{
	int i, j;
	unsigned char *pixel = surface->pixels;
	for(i = 0; i < surface->w; i++)
		for(j = 0; j < surface->h; j++)
		{
			*(pixel + 1) = 0x80;
			pixel += 4;
		}
}

void test_preview(SDL_Surface *surface, char *file)
{
	unsigned char *yuv = read_file(file);
	int i, j;
	int width = WIDTH;
	int height = HEIGHT;
	unsigned char *pixel = surface->pixels;
	for(i = 0; i < height; i++)
		for(j = 0; j < width; j++)
		{
			*pixel = *yuv;
			*(pixel+1) = *yuv;
			*(pixel+2) = *yuv;
			pixel += 4;
			yuv++;
		}
}

void rgb888_to_rgb8888(char *src, char *dst, int width, int height)
{
	int pixel = width*height;
	memset(dst, 0, pixel*4);
	while(pixel--)
	{
		dst[0]=src[0];
		dst[1]=src[1];
		dst[2]=src[2];
		src+=3;
		dst+=4;
	}
}

void test_rgb(SDL_Surface *surface)
{
	unsigned char *rgb = read_file("1.rgb");
	rgb888_to_rgb8888(rgb, rgb8888, 3264, 2448);
	int i, j;
	rgb_scale(rgb_s, rgb8888, WIDTH, HEIGHT,3264, 2448);
	int width = WIDTH;
	int height = HEIGHT;
	unsigned char *pixel = surface->pixels;
	rgb = rgb_s;
	for(i = 0; i < height; i++)
		for(j = 0; j < width; j++)
		{
			*pixel = *(rgb + 0);
			*(pixel+1) = *(rgb+1);
			*(pixel+2) = *(rgb+2);
			rgb += 4;
			pixel += 4;
		}
}

void showDisplay(SDL_Surface *screen, SDL_Surface *src)
{
	memcpy(screen->pixels, src->pixels, src->w * src->h * 4);
	SDL_Flip(screen);
}

int Destory(SDL_Surface *file)
{
	SDL_FreeSurface( file );
	return 0;
}

int test_previews(SDL_Surface *screen, SDL_Surface *src)
{
	char name[100];
	int i, last = 160;
	for(i = 1; i < last; i++)
	{
		sprintf(name, "%d.yuv", i);
		printf("show %s\n", name);
		test_preview(src, name);
		showDisplay(screen, src);
		SDL_Delay(1000);
	}
}

int main(int argc,char **argv)
{
	SDL_Surface *screen;
	int width = WIDTH;
	int height = HEIGHT;
	int bpp = 32;
	Init();
	screen = createScreen(width , height, bpp , SDL_SWSURFACE);
	SDL_Delay(10);

	test_rgb(screen);
	SDL_Flip(screen);
	SDL_Delay(5000);
	Destory(screen);
	SDL_Quit();
	return 0;
}
