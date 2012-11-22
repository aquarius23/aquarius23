#ifndef _LOG_H
#define _LOG_H

#define CB_LOGV (1 << 0)
#define CB_LOGD (1 << 1)
#define CB_LOGE (1 << 2)
#define CB_LOGW (1 << 3)
#define CB_LOGI (1 << 4)
#define CB_LOGH (1 << 5)

void __sdl_log(int tag, const char *fmt, ...);
#define LOGD(...) __sdl_log(CB_LOGD, __VA_ARGS__)
#define LOGE(...) __sdl_log(CB_LOGE, __VA_ARGS__)
#define LOGI(...) __sdl_log(CB_LOGI, __VA_ARGS__)
#define LOGW(...) __sdl_log(CB_LOGW, __VA_ARGS__)
#define LOGV(...) __sdl_log(CB_LOGV, __VA_ARGS__)
#endif

