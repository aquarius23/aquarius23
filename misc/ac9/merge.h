#ifndef _MERGE_H
#define _MERGE_H
int shlaAutoFix(unsigned char *inData, unsigned char *outData, int width, int height);
int shlaHDR(unsigned char **inData, unsigned char *outData, int *width, int *height);
int shlaLowLight(unsigned char **inData, unsigned char *outData, int *width, int *height);
#endif

