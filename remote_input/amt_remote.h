#ifndef _AMT_REMOTE_H
#define _AMT_REMOTE_H

#define SERVER_PORT 11220

#define CB_LOGV	(1 << 0)
#define CB_LOGD	(1 << 1)
#define CB_LOGE	(1 << 2)
#define CB_LOGW	(1 << 3)
#define CB_LOGI	(1 << 4)
#define CB_LOGA	(CB_LOGV | CB_LOGD | CB_LOGE | CB_LOGW | CB_LOGI)

typedef void (*amt_log_callback)(int tag, const char *log);
void amt_log_register(amt_log_callback cb);
void amt_log_control(int tag_on);

int init_server_sock(void);
int init_client_sock(void);
int connect_server(char *ip, int port);
#endif

