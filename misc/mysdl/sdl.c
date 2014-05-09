#include "SDL/SDL.h"

#define WIDTH 1024
#define HEIGHT 768
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

int main(int argc,char **argv)
{
	SDL_Surface *screen;
	SDL_Surface *bmp;
	int width = WIDTH;
	int height = HEIGHT;
	int bpp = 32;
	Init();
	screen = createScreen(width , height, bpp , SDL_SWSURFACE);
	bmp = create_surface(width, height);

	test_draw(bmp);
	showDisplay(screen, bmp);
	SDL_Delay(2000);
	Destory(bmp);
	Destory(screen);
	SDL_Quit();
	return 0;
}
