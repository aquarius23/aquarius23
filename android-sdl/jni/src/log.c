#include <stdio.h>
#include <stdarg.h>
#include "log.h"

#undef LOG_TAG
#define LOG_TAG "SDL"
#ifdef __ANDROID__
#include <android/log.h>
void __print_log(int tag, const char *log)
{
	switch(tag)
	{
		case CB_LOGD:
			tag = ANDROID_LOG_DEBUG;
			break;
		case CB_LOGE:
			tag = ANDROID_LOG_ERROR;
			break;
		case CB_LOGI:
			tag = ANDROID_LOG_INFO;
			break;
		case CB_LOGW:
			tag = ANDROID_LOG_WARN;
			break;
		case CB_LOGV:
			tag = ANDROID_LOG_VERBOSE;
			break;
		default:
			tag = ANDROID_LOG_VERBOSE;
			break;
	}
	__android_log_print(tag, LOG_TAG, log);
}
#else
void __print_log(int tag, const char *log)
{
	char *s_tag;
	switch(tag)
	{
		case CB_LOGD:
			s_tag = "LOGD";
			break;
		case CB_LOGE:
			s_tag = "LOGE";
			break;
		case CB_LOGI:
			s_tag = "LOGI";
			break;
		case CB_LOGW:
			s_tag = "LOGW";
			break;
		case CB_LOGV:
			s_tag = "LOGV";
			break;
		default:
			s_tag = "LOGV";
			break;
	}
	printf("%s:%s:%s", s_tag, LOG_TAG, log);
}
#endif

void __sdl_log(int tag, const char *fmt, ...)
{
	va_list ap;
	char buf[1024];
	va_start(ap, fmt);
	vsnprintf(buf, 1024, fmt, ap);
	va_end(ap);
	__print_log(tag, buf);
}

