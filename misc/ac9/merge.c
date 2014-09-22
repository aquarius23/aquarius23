#include <stdio.h>
#include <stdlib.h>

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
	matrix = (double**)SHLA_MemAlloc(sizeof(double*)*itemsCount);
	for (i = 0; i < itemsCount; i++)
		matrix[i] = (double*)SHLA_MemAlloc(sizeof(double)*9);

	CHECKALIGN(SHLA_ALIGN(src, 0, itemsCount, &rect, matrix));

	for (i = 0; i < itemsCount; i++)
	{
		srcAllign[i]->dwPixelFormat = src[0]->dwPixelFormat;
		srcAllign[i]->lWidth = rect.right - rect.left + 1;
		srcAllign[i]->lHeight = rect.bottom - rect.top + 1;
		srcAllign[i]->lPitch[0] = srcAllign[i]->lWidth*3;
		srcAllign[i]->pPlane[0] = (unsigned char*)SHLA_MemAlloc(srcAllign[i]->lPitch[0]*srcAllign[i]->lHeight);
	}
	CHECKALIGN(SHLA_XFORM(src, itemsCount, &rect, matrix, srcAllign));
EXIT:
	for(i=0; i<itemsCount; i++)
	{
		SHLA_MemFree(matrix[i]);
	}
	SHLA_MemFree(matrix);

	return res;
}

/*int shlaAutoFix()
{
	int res = 0;
	BMPINFO src = {0};
	BMPINFO dst = {0};
	int w = 1280;
	int h = 720;
	int size = (w*h*3)/2;
	char *srcdata = new char[size];
	unsigned char* outData = NULL;
	unsigned char* inData = NULL;
	char* outFilePath = NULL;
	cout << "------------------ AUTOFIX Effect is start ------------------" << endl;
	
	readFile("/home/cwx/shla/testbed_linux/data/src_autofix/1280x720.i420", size, srcdata);
  outData = (unsigned char*)SHLA_MemAlloc(size);
  inData = (unsigned char*)srcdata;
  
	src.dwPixelFormat = BMPFORMAT_YCBCR_I420;
	src.lWidth  = w;
	src.lHeight = h;
	src.lPitch[0] = w;
	src.lPitch[1] = w/2;
	src.lPitch[2] = w/2;
	src.pPlane[0] = inData;
	src.pPlane[1] = inData + w * h;
	src.pPlane[2] = inData + w * h + (w * h)/4;

	dst.dwPixelFormat = BMPFORMAT_YCBCR_I420;
	dst.lWidth  = w;
	dst.lHeight = h;
	dst.lPitch[0] = w;
	dst.lPitch[1] = w/2;
	dst.lPitch[2] = w/2;
	dst.pPlane[0] = outData;
	dst.pPlane[1] = outData + w * h;
	dst.pPlane[2] = outData + w * h + (w * h)/4;
	
	CHECK(SHLA_Autofix(&src, &dst));
	
	outFilePath = getOutPath(dst.lWidth, dst.lHeight, "_AUTOFIX", ".I420");
	cout << "outFilePath is: "<< outFilePath << endl;
	saveFile(outFilePath, size, (const char*)outData);
EXIT:
	if(NULL != outData)
		SHLA_MemFree(outData);
	if(res == 0)
		cout << "AUTOFIX effect is success" << endl;
	else
		cout << "AUTOFIX effect is error res = "<< res << endl;
	cout << "------------------ AUTOFIX Effect is end ------------------" << endl;
  return res;
}*/

/*int shlaHDR()
{
	int res 								= 0;
	int w 									= 1280;
	int h 									= 720;
	int size 								= w*h*3;
	int index 							= 3;
	BMPINFO **src 					= 0;
	BMPINFO **srcAllign 		= 0;
	char* outFilePath 			= NULL;
	BMPINFO dst 						= {0};
	unsigned char* outData 	= NULL;
	unsigned char** inData;

	cout << "------------------ HDR Effect is start ------------------" << endl;
	inData = (unsigned char **)SHLA_MemAlloc(sizeof(unsigned char*)*index*size);
  for( int i=0; i<index; i++)
  {
  	inData[i] = (unsigned char *)SHLA_MemAlloc(size);
  }
	readFile("/home/cwx/shla/testbed_linux/data/src_hdr/1280X720_0.RGB24", size, (char*)inData[0]);
	readFile("/home/cwx/shla/testbed_linux/data/src_hdr/1280X720_1.RGB24", size, (char*)inData[1]);
  readFile("/home/cwx/shla/testbed_linux/data/src_hdr/1280X720_2.RGB24", size, (char*)inData[2]);
  
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
  CHECK(shla_align(src, srcAllign, index));
	outData = (unsigned char*)SHLA_MemAlloc(srcAllign[0]->lPitch[0] * srcAllign[0]->lHeight);
	size = srcAllign[0]->lWidth * srcAllign[0]->lHeight * 3;

	dst.dwPixelFormat = srcAllign[0]->dwPixelFormat;
	dst.lWidth = srcAllign[0]->lWidth;
	dst.lHeight = srcAllign[0]->lHeight;
	dst.lPitch[0] = srcAllign[0]->lPitch[0];
	dst.pPlane[0] = outData;
	printf("dst picture size width: %d, height: %d \n", dst.lWidth, dst.lHeight);

	CHECK(SHLA_HDR(srcAllign, 0, index, &dst));

	outFilePath = getOutPath(dst.lWidth, dst.lHeight, "_HDR", ".RGB24");
  cout << "outFilePath is: "<< outFilePath << endl;
  saveFile(outFilePath, size, (const char*)outData);

EXIT:
	if(NULL != outData)
		SHLA_MemFree(outData);
	for( int i=0; i<index; i++)
	{
		SHLA_MemFree(inData[i]);
		SHLA_MemFree(src[i]);
		if(NULL != srcAllign[i]->pPlane[0])
			SHLA_MemFree(srcAllign[i]->pPlane[0]);
		SHLA_MemFree(srcAllign[i]);
	}
	SHLA_MemFree(inData);
	SHLA_MemFree(src);
	SHLA_MemFree(srcAllign);
	if(res == 0)
		cout << "HDR effect is success" << endl;
	else
		cout << "HDR effect is error res = "<< res << endl;
	cout << "------------------ HDR Effect is end   ------------------" << endl;
  return res;
}*/

int shlaLowLight(unsigned char **inData, unsigned char *outData, int *width, int *height)
{
	int i;
	int res 							= 0;
	int w 								= *width;
	int h 								= *height;
	int size 							= w*h*3;
	int index 						= 4;
	BMPINFO **src 				= 0;
	BMPINFO **srcAllign 	= 0;
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
	CHECK(shla_align(src, srcAllign, index));
	size = srcAllign[0]->lWidth * srcAllign[0]->lHeight * 3;
	dst.dwPixelFormat = srcAllign[0]->dwPixelFormat;
	dst.lWidth = srcAllign[0]->lWidth;
	dst.lHeight = srcAllign[0]->lHeight;
	dst.lPitch[0] = srcAllign[0]->lPitch[0];
	dst.pPlane[0] = outData;
	printf("dst picture size width: %d, height: %d \n", dst.lWidth, dst.lHeight);
	*width = dst.lWidth;
	*height = dst.lHeight;
	CHECK(SHLA_Lowlight(srcAllign, 0, index, &dst));

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
			printf("LOWLIGHT effect is success\n");
	else
		printf("LOWLIGHT effect is error res = %d\n ", res);
  return res;
}

