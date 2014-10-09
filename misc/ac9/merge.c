#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "shla.h"

#define MOK								0

#define CHECK(x) if (MOK != (res = x)) goto EXIT
	
#define CHECKALIGN(x) if (-1 == (res = x)) goto EXIT

#define UpAlign4(n) (((n) + 3) & ~3)

static void* SHLA_MemAlloc(long size);
static void SHLA_MemFree(void* pMem);
static int shla_align(BMPINFO **src, BMPINFO **srcAllign, int itemsCount);
//static int shlaAutoFix();
//static int shlaHDR();
//static int shlaLowLight();

void* SHLA_MemAlloc(long size)
{
	return malloc(size);
}

void SHLA_MemFree(void* pMem)
{
	free(pMem);
}

int shla_align(BMPINFO **src, BMPINFO **srcAllign, int itemsCount)
{
	int i, res = 0;
	double** matrix;
	SHLARECT rect 		= {0};
	long imageRef       = 0;
	matrix = (double**)SHLA_MemAlloc(sizeof(double*)*itemsCount);
	for (i = 0; i < itemsCount; i++)
		matrix[i] = (double*)SHLA_MemAlloc(sizeof(double)*9);

	//CHECKALIGN(SHLA_ALIGN(src, 0, itemsCount, &rect, matrix));
	res = SHLA_ALIGN(src, 0, itemsCount, &rect, matrix, &imageRef);
	if (res == 0)
	{
		for (int i = 0; i < itemsCount; i++)
		{
			srcAllign[i]->dwPixelFormat = src[0]->dwPixelFormat;
			srcAllign[i]->lWidth = rect.right - rect.left + 1;
			srcAllign[i]->lHeight = rect.bottom - rect.top + 1;
			srcAllign[i]->lPitch[0] = srcAllign[i]->lWidth*3;
			srcAllign[i]->pPlane[0] = (unsigned char*)SHLA_MemAlloc(srcAllign[i]->lPitch[0]*srcAllign[i]->lHeight);
		}
		CHECKALIGN(SHLA_XFORM(src, itemsCount, &rect, matrix, srcAllign));
	}
	else if (res == 1 && imageRef < itemsCount)
	{
			srcAllign[0]->dwPixelFormat = src[imageRef]->dwPixelFormat;
			srcAllign[0]->lWidth = src[imageRef]->lWidth;
			srcAllign[0]->lHeight = src[imageRef]->lHeight;
			srcAllign[0]->lPitch[0] = UpAlign4(srcAllign[0]->lWidth*3);
			srcAllign[0]->pPlane[0] = src[imageRef]->pPlane[0];
	}

EXIT:
	for(i=0; i<itemsCount; i++)
	{
		SHLA_MemFree(matrix[i]);
	}
	SHLA_MemFree(matrix);

	printf("align return value = %d\n", res);
	return res;
}

int shlaAutoFix(unsigned char *inData, unsigned char *outData, int width, int height)
{
	int res = 0;
	BMPINFO src = {0};
	BMPINFO dst = {0};
	int w = width;
	int h = height;

	src.dwPixelFormat = BMPFORMAT_RGB24_R8G8B8;
	src.lWidth  = w;
	src.lHeight = h;
	src.lPitch[0] = w * 3;
	src.pPlane[0] = inData;

	dst.dwPixelFormat = src.dwPixelFormat;
	dst.lWidth = src.lWidth;
	dst.lHeight = src.lHeight;
	dst.lPitch[0] = src.lPitch[0];
	dst.pPlane[0] = outData;

	CHECK(SHLA_Autofix(&src, &dst));
EXIT:
	if(res == 0)
		printf("AUTOFIX effect is success\n");
	else
		printf("AUTOFIX effect is error res = %d\n", res);
  return res;
}

int shlaHDR(unsigned char **inData, unsigned char *outData, int *width, int *height)
{
	int i;
	int res 								= 0;
	int allignRes							= 0;
	int w 									= *width;
	int h 									= *height;
	int size 								= w*h*3;
	int index 							= 3;
	BMPINFO **src 					= 0;
	BMPINFO **srcAllign 		= 0;
	BMPINFO dst 						= {0};
  
	srcAllign = (BMPINFO **)SHLA_MemAlloc(sizeof(BMPINFO*)*index);
	src = (BMPINFO **)SHLA_MemAlloc(sizeof(BMPINFO*)*index);
	for( int i=0; i<index; i++)
	{
		srcAllign[i] = (BMPINFO *)SHLA_MemAlloc(sizeof(BMPINFO));
		srcAllign[i]->pPlane[0] = NULL;
		src[i] = (BMPINFO*)SHLA_MemAlloc(sizeof(BMPINFO));
		src[i]->dwPixelFormat = BMPFORMAT_RGB24_R8G8B8;
		src[i]->lWidth = w;
		src[i]->lHeight = h;
		src[i]->lPitch[0] = w*3;
		src[i]->pPlane[0] = inData[i];
	}
	//CHECK(shla_align(src, srcAllign, index));
	allignRes = shla_align(src, srcAllign, index);
	size = srcAllign[0]->lWidth * srcAllign[0]->lHeight * 3;

	dst.dwPixelFormat = srcAllign[0]->dwPixelFormat;
	dst.lWidth = srcAllign[0]->lWidth;
	dst.lHeight = srcAllign[0]->lHeight;
	dst.lPitch[0] = srcAllign[0]->lPitch[0];
	dst.pPlane[0] = outData;
	printf("dst picture size width: %d, height: %d \n", dst.lWidth, dst.lHeight);
	if (allignRes == 0)
	{
		CHECK(SHLA_HDR(srcAllign, 0, index, &dst));
	}
	else if (allignRes == 1)
	{
		memcpy(outData, srcAllign[0]->pPlane[0], dst.lPitch[0]*dst.lHeight);
		outData = srcAllign[0]->pPlane[0];
	}
	*width = dst.lWidth;
	*height = dst.lHeight;

EXIT:
	for(i=0; i<index; i++)
	{
		SHLA_MemFree(src[i]);
		if(NULL != srcAllign[i]->pPlane[0])
			SHLA_MemFree(srcAllign[i]->pPlane[0]);
		SHLA_MemFree(srcAllign[i]);
	}
	SHLA_MemFree(src);
	SHLA_MemFree(srcAllign);
	if(res == 0)
		printf("HDR effect is success\n");
	else
		printf("HDR effect is error res = %d\n", res);
	return res;
}

int shlaLowLight(unsigned char **inData, unsigned char *outData, int *width, int *height)
{
	int i;
	int res 							= 0;
	int allignRes						= 0;
	int w 								= *width;
	int h 								= *height;
	int size 							= w*h*3;
	int index 						= 4;
	BMPINFO **src 				= 0;
	BMPINFO **srcAllign 	= 0;
	BMPINFO **srcAllignFail = 0;
	BMPINFO dst 					= {0};
	
	srcAllign = (BMPINFO **)SHLA_MemAlloc(sizeof(BMPINFO*)*index);
	src = (BMPINFO **)SHLA_MemAlloc(sizeof(BMPINFO*)*index);
	for(i=0; i<index; i++)
	{
		srcAllign[i] = (BMPINFO *)SHLA_MemAlloc(sizeof(BMPINFO));
	  	srcAllign[i]->pPlane[0] = NULL;
	    src[i] = (BMPINFO*)SHLA_MemAlloc(sizeof(BMPINFO));
		src[i]->dwPixelFormat = BMPFORMAT_RGB24_R8G8B8;
		src[i]->lWidth = w;
		src[i]->lHeight = h;
		src[i]->lPitch[0] = w*3;
		src[i]->pPlane[0] = inData[i];
	}
	//CHECK(shla_align(src, srcAllign, index));
	allignRes = shla_align(src, srcAllign, index);
	size = srcAllign[0]->lWidth * srcAllign[0]->lHeight * 3;
	dst.dwPixelFormat = srcAllign[0]->dwPixelFormat;
	dst.lWidth = srcAllign[0]->lWidth;
	dst.lHeight = srcAllign[0]->lHeight;
	dst.lPitch[0] = srcAllign[0]->lPitch[0];
	dst.pPlane[0] = outData;
	printf("dst picture size width: %d, height: %d \n", dst.lWidth, dst.lHeight);
	*width = dst.lWidth;
	*height = dst.lHeight;

	if (allignRes == 0)
	{
		CHECK(SHLA_Lowlight(srcAllign, 0, index, &dst));
	}
	else if (allignRes == 1)
	{
		srcAllignFail = (BMPINFO **)SHLA_MemAlloc(sizeof(BMPINFO*)*1);
		srcAllignFail[0] = (BMPINFO *)SHLA_MemAlloc(sizeof(BMPINFO));
		srcAllignFail[0]->dwPixelFormat = srcAllign[0]->dwPixelFormat;
		srcAllignFail[0]->lWidth = srcAllign[0]->lWidth;
		srcAllignFail[0]->lHeight = srcAllign[0]->lHeight;
		srcAllignFail[0]->lPitch[0] = srcAllign[0]->lPitch[0];
		srcAllignFail[0]->pPlane[0] = srcAllign[0]->pPlane[0];

		CHECK(SHLA_Lowlight(srcAllignFail, 0, 1, &dst));
	}
EXIT:
	for(i=0; i<index; i++)
	{
		SHLA_MemFree(src[i]);
		if(NULL != srcAllign[i]->pPlane[0])
			SHLA_MemFree(srcAllign[i]->pPlane[0]);
		SHLA_MemFree(srcAllign[i]);
	}
	if (allignRes == 1)
	{
		SHLA_MemFree(srcAllignFail[0]);
		SHLA_MemFree(srcAllignFail);
	}
	SHLA_MemFree(src);
	SHLA_MemFree(srcAllign);
	if(res == 0)
		printf("LOWLIGHT effect is success\n");
	else
		printf("LOWLIGHT effect is error res = %d\n ", res);
  return res;
}

