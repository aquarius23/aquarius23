#include <SDL.h>
#include "log.h"
#ifdef WIN32
#include <windows.h>
#endif

static void print_renderer_flag(Uint32 flag)
{
	switch(flag)
	{
		case SDL_RENDERER_PRESENTVSYNC:
			LOGD("%s PresentVSync\n", __func__);
			break;
		case SDL_RENDERER_ACCELERATED:
			LOGD("%s Accelerated\n", __func__);
			break;
		default:
			LOGD("%s 0x%8.8x\n", __func__, flag);
			break;
	}
}

static void print_pixel_format(Uint32 format)
{
	LOGD("%s: ", __func__);
	switch(format)
	{
		case SDL_PIXELFORMAT_UNKNOWN:
			LOGD("Unknwon");
			break;
		case SDL_PIXELFORMAT_INDEX1LSB:
			LOGD("Index1LSB");
			break;
		case SDL_PIXELFORMAT_INDEX1MSB:
			LOGD("Index1MSB");
			break;
		case SDL_PIXELFORMAT_INDEX4LSB:
			LOGD("Index4LSB");
			break;
		case SDL_PIXELFORMAT_INDEX4MSB:
			LOGD("Index4MSB");
			break;
		case SDL_PIXELFORMAT_INDEX8:
			LOGD("Index8");
			break;
		case SDL_PIXELFORMAT_RGB332:
			LOGD("RGB332");
			break;
		case SDL_PIXELFORMAT_RGB444:
			LOGD("RGB444");
			break;
		case SDL_PIXELFORMAT_RGB555:
			LOGD("RGB555");
			break;
		case SDL_PIXELFORMAT_BGR555:
			LOGD("BGR555");
			break;
		case SDL_PIXELFORMAT_ARGB4444:
			LOGD("ARGB4444");
			break;
		case SDL_PIXELFORMAT_ABGR4444:
			LOGD("ABGR4444");
			break;
		case SDL_PIXELFORMAT_ARGB1555:
			LOGD("ARGB1555");
			break;
		case SDL_PIXELFORMAT_ABGR1555:
			LOGD("ABGR1555");
			break;
		case SDL_PIXELFORMAT_RGB565:
			LOGD("RGB565");
			break;
		case SDL_PIXELFORMAT_BGR565:
			LOGD("BGR565");
			break;
		case SDL_PIXELFORMAT_RGB24:
			LOGD("RGB24");
			break;
		case SDL_PIXELFORMAT_BGR24:
			LOGD("BGR24");
			break;
		case SDL_PIXELFORMAT_RGB888:
			LOGD("RGB888");
			break;
		case SDL_PIXELFORMAT_BGR888:
			LOGD("BGR888");
			break;
		case SDL_PIXELFORMAT_ARGB8888:
			LOGD("ARGB8888");
			break;
		case SDL_PIXELFORMAT_RGBA8888:
			LOGD("RGBA8888");
			break;
		case SDL_PIXELFORMAT_ABGR8888:
			LOGD("ABGR8888");
			break;
		case SDL_PIXELFORMAT_BGRA8888:
			LOGD("BGRA8888");
			break;
		case SDL_PIXELFORMAT_ARGB2101010:
			LOGD("ARGB2101010");
			break;
		case SDL_PIXELFORMAT_YV12:
			LOGD("YV12");
			break;
		case SDL_PIXELFORMAT_IYUV:
			LOGD("IYUV");
			break;
		case SDL_PIXELFORMAT_YUY2:
			LOGD("YUY2");
			break;
		case SDL_PIXELFORMAT_UYVY:
			LOGD("UYVY");
			break;
		case SDL_PIXELFORMAT_YVYU:
			LOGD("YVYU");
			break;
		default:
			LOGD("0x%8.8x", format);
			break;
	}
	LOGD("\n");
}

static void print_renderer(SDL_RendererInfo * info)
{
	int i, count;
	LOGD("  Renderer %s:\n", info->name);
	LOGD("    Flags: 0x%8.8X\n", info->flags);
	count = 0;
	for(i = 0; i < sizeof(info->flags) * 8; ++i)
	{
		Uint32 flag = (1 << i);
		if(info->flags & flag)
		{
			print_renderer_flag(flag);
			++count;
		}
	}
	LOGD("    Texture formats (%d): \n", info->num_texture_formats);
	for(i = 0; i < (int)info->num_texture_formats; ++i)
		print_pixel_format(info->texture_formats[i]);
	if(info->max_texture_width || info->max_texture_height)
		LOGD("    Max Texture Size: %dx%d\n",  info->max_texture_width, info->max_texture_height);
}

void enum_video_driver(void)
{
	int i, n;
	n = SDL_GetNumVideoDrivers();
	if(n > 0)
	{
		for(i = 0; i < n; ++i)
			LOGD("%s: %s\n", __func__, SDL_GetVideoDriver(i));
	}

}

void enum_display(void)
{
	int i, j, m, n;
	SDL_Rect bounds;
	SDL_DisplayMode mode;
	int bpp;
	Uint32 Rmask, Gmask, Bmask, Amask;

	n = SDL_GetNumVideoDisplays();
	LOGD("Number of displays: %d\n", n);
	for(i = 0; i < n; ++i)
	{
		SDL_zero(bounds);
		SDL_GetDisplayBounds(i, &bounds);
		LOGD("Bounds: %dx%d at %d,%d\n", bounds.w, bounds.h, bounds.x, bounds.y);
		SDL_GetDesktopDisplayMode(i, &mode);
		SDL_PixelFormatEnumToMasks(mode.format, &bpp, &Rmask, &Gmask, &Bmask, &Amask);
		LOGD("  Current mode: %dx%d@%dHz, %d bits-per-pixel (%s)\n",
                        mode.w, mode.h, mode.refresh_rate, bpp,
                        SDL_GetPixelFormatName(mode.format));
		if(Rmask || Gmask || Bmask)
		{
			LOGD("      Red Mask   = 0x%.8x\n", Rmask);
			LOGD("      Green Mask = 0x%.8x\n", Gmask);
			LOGD("      Blue Mask  = 0x%.8x\n", Bmask);
			if(Amask)
				LOGD("      Alpha Mask = 0x%.8x\n", Amask);
		}

		m = SDL_GetNumDisplayModes(i);
		if(m == 0)
			LOGE("No available fullscreen video modes\n");
		else
		{
			LOGD("  Fullscreen video modes:\n");
			for (j = 0; j < m; ++j)
			{
				SDL_GetDisplayMode(i, j, &mode);
				SDL_PixelFormatEnumToMasks(mode.format, &bpp, &Rmask, &Gmask, &Bmask, &Amask);
				LOGD("    Mode %d: %dx%d@%dHz, %d bits-per-pixel (%s)\n",
					j, mode.w, mode.h, mode.refresh_rate, bpp,
					SDL_GetPixelFormatName(mode.format));
				if(Rmask || Gmask || Bmask)
				{
					LOGD("        Red Mask   = 0x%.8x\n", Rmask);
					LOGD("        Green Mask = 0x%.8x\n", Gmask);
					LOGD("        Blue Mask  = 0x%.8x\n", Bmask);
					if(Amask)
						LOGD("        Alpha Mask = 0x%.8x\n", Amask);
				}
			}
		}
	}
	
	n = SDL_GetNumRenderDrivers();
	for(i = 0; i < n; ++i)
	{
		SDL_RendererInfo info;
		SDL_GetRenderDriverInfo(i, &info);
		print_renderer(&info);
	}
}

int main(int argc, char *argv[])
{
	int ret;
	enum_video_driver();
	ret = SDL_VideoInit(NULL);
	if(ret < 0)
		return 0;
	enum_display();	
	return 1;
}

#ifdef WIN32
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	char *argv = "sdl";
	return main(1, &argv);
}
#endif
