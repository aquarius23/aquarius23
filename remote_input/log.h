#ifndef _LOG_H
#define _LOG_H

#include "amt_remote.h"
void __amt_log(int tag, const char *fmt, ...);
#define LOGD(...) __amt_log(CB_LOGD, __VA_ARGS__)
#define LOGE(...) __amt_log(CB_LOGE, __VA_ARGS__)
#define LOGI(...) __amt_log(CB_LOGI, __VA_ARGS__)
#define LOGW(...) __amt_log(CB_LOGW, __VA_ARGS__)
#define LOGV(...) __amt_log(CB_LOGV, __VA_ARGS__)

#endif

