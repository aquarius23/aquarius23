#include <stdio.h>
#include <stdarg.h>
#include "log.h"

static int g_log_flag = 0;
static amt_log_callback g_log_cb = NULL;

void __amt_log(int tag, const char *fmt, ...)
{
	if(g_log_cb && (g_log_flag & tag))
	{
		va_list ap;
		char buf[1024];
		va_start(ap, fmt);
		vsnprintf(buf, 1024, fmt, ap);
		va_end(ap);
		g_log_cb(tag, buf);
	}
}

void amt_log_register(amt_log_callback cb)
{
	g_log_cb = cb;
}

void amt_log_control(int tag_on)
{
	g_log_flag = tag_on & CB_LOGA;
}

