#ifndef _SHLA_H_
#define _SHLA_H_

#ifdef __cplusplus
extern "C" {
#endif

#define IN
#define OUT

#define SCENE_NORMAL	0
#define SCENE_HDR		1
#define SCENE_LOWLIGHT	2
#define SCENE_OVEREXPOSURE		3

	typedef struct _tag_shootinfo
	{
		int lExposureTime;
		int lISO;
		float focus;
	}SHOOTINFO, *LPSHOOTINFO;

	typedef struct _tag_sensorinfo
	{
		float fYaw;
		float fRoll;
		float fPitch;
	}SENSORINFO, *LPSENSORINFO;

	typedef struct _tag_imageinfo
	{
		SHOOTINFO shootInfo;
		SENSORINFO sensorInfo;
	}IMAGEINFO, *LPIMAGEINFO;

#define BMPFORMAT_GRAY8			0
#define BMPFORMAT_RGB24_R8G8B8	1
#define BMPFORMAT_YCBCR_NV12	2
#define BMPFORMAT_YCBCR_I420	3

	typedef struct __tag_bmpinfo
	{
		unsigned int dwPixelFormat;
		int lWidth;
		int lHeight;
		int lPitch[3];
		unsigned char* pPlane[3];
	}BMPINFO, *LPBMPINFO;

#define DEFAULTEXPOSURETIME 0
#define DEFAULTISO 0

#define MAX_CAPTURENUMBER 5

	typedef struct __tag_captureMode
	{
		unsigned int dwCaptureNum;
		int lExposureTime[MAX_CAPTURENUMBER];
		int lISO[MAX_CAPTURENUMBER];
	}CAPTUREMODE, *LPCAPTUREMODE;

	typedef struct __tag_SHLA_RECT
	{
		int left, right;
		int top,bottom;
	}SHLARECT, *LPSHLARECT;

	int SHLA_Detection(IN BMPINFO *pSrcBitmap, IN IMAGEINFO *pImageInfo, IN long lLowLightISOThreshold, OUT unsigned int *pdwSceneMode, OUT CAPTUREMODE *pCaptureMode);
	int SHLA_Autofix(IN BMPINFO *pSrcBitmap, OUT BMPINFO *pDstBitmap);
	int SHLA_HDR(IN BMPINFO **ppSrcBitmap, IN IMAGEINFO **ppImageInfo, IN int lBitmapCnt, OUT BMPINFO *pDstBitmap);
	int SHLA_Lowlight(IN BMPINFO **ppSrcBitmap, IN IMAGEINFO **ppImageInfo, IN int lBitmapCnt, OUT BMPINFO *pDstBitmap);

	int SHLA_ALIGN(IN BMPINFO **pSrcBitmap, IN IMAGEINFO **ppImageInfo, IN int lBitmapCnt, OUT LPSHLARECT p_mRect, OUT double **ppMatrix, OUT long *pImageReference);
	int SHLA_XFORM(IN BMPINFO **pSrcBitmap, IN int lBitmapCnt, IN LPSHLARECT p_mRect, IN double **ppMatrix, IN OUT BMPINFO **pDstBitmap);

#ifdef __cplusplus
}
#endif

#endif //_SCENEDETECT_H_
