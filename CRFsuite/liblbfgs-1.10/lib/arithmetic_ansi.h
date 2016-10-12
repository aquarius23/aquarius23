/*
 *      ANSI C implementation of vector operations.
 *
 * Copyright (c) 2007-2010 Naoaki Okazaki
 * All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/* $Id$ */

#include <stdlib.h>
#include <memory.h>
#include <pthread.h>

#if     LBFGS_FLOAT == 32 && LBFGS_IEEE_FLOAT
#define fsigndiff(x, y) (((*(uint32_t*)(x)) ^ (*(uint32_t*)(y))) & 0x80000000U)
#else
#define fsigndiff(x, y) (*(x) * (*(y) / fabs(*(y))) < 0.)
#endif/*LBFGS_IEEE_FLOAT*/

inline static void* vecalloc(size_t size)
{
    void *memblock = malloc(size);
    if (memblock) {
        memset(memblock, 0, size);
    }
    return memblock;
}

inline static void vecfree(void *memblock)
{
    free(memblock);
}

#define MULTI_THREAD
#ifndef MULTI_THREAD
inline static void vecset(lbfgsfloatval_t *x, const lbfgsfloatval_t c, const int n)
{
    int i;
    
    for (i = 0;i < n;++i) {
        x[i] = c;
    }
}

inline static void veccpy(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const int n)
{
    int i;

    for (i = 0;i < n;++i) {
        y[i] = x[i];
    }
}

inline static void vecncpy(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const int n)
{
    int i;

    for (i = 0;i < n;++i) {
        y[i] = -x[i];
    }
}

inline static void vecadd(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const lbfgsfloatval_t c, const int n)
{
    int i;

    for (i = 0;i < n;++i) {
        y[i] += c * x[i];
    }
}

inline static void vecdiff(lbfgsfloatval_t *z, const lbfgsfloatval_t *x, const lbfgsfloatval_t *y, const int n)
{
    int i;

    for (i = 0;i < n;++i) {
        z[i] = x[i] - y[i];
    }
}

inline static void vecscale(lbfgsfloatval_t *y, const lbfgsfloatval_t c, const int n)
{
    int i;

    for (i = 0;i < n;++i) {
        y[i] *= c;
    }
}

inline static void vecmul(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const int n)
{
    int i;

    for (i = 0;i < n;++i) {
        y[i] *= x[i];
    }
}

inline static void vecdot(lbfgsfloatval_t* s, const lbfgsfloatval_t *x, const lbfgsfloatval_t *y, const int n)
{
    int i;
    *s = 0.;
    for (i = 0;i < n;++i) {
        *s += x[i] * y[i];
    }
}

inline static void vec2norm(lbfgsfloatval_t* s, const lbfgsfloatval_t *x, const int n)
{
    vecdot(s, x, x, n);
    *s = (lbfgsfloatval_t)sqrt(*s);
}

inline static void vec2norminv(lbfgsfloatval_t* s, const lbfgsfloatval_t *x, const int n)
{
    vec2norm(s, x, n);
    *s = (lbfgsfloatval_t)(1.0 / *s);
}

void ansi_init(void)
{
}

#else
#define THREAD_NUMBER 4
#define VECSET 1
#define VECCPY 2
#define VECNCPY 3
#define VECADD 4
#define VECDIFF 5
#define VECSCALE 6
#define VECMUL 7
#define VECDOT 8
static int first = 1;
static pthread_t pid_thread[THREAD_NUMBER];
static pthread_mutex_t mutex[THREAD_NUMBER];
static pthread_cond_t cond[THREAD_NUMBER];
static pthread_mutex_t op_mutex;
static pthread_cond_t op_cond;
static lbfgsfloatval_t arg_c, *arg_v[3];
static lbfgsfloatval_t temp_dot[THREAD_NUMBER];
static int arg_n;
static int arg_op;
static int op_count;
static void submit_thread(lbfgsfloatval_t *arg1, lbfgsfloatval_t *arg2, lbfgsfloatval_t *arg3, lbfgsfloatval_t c, const int n, const int op)
{
	pthread_mutex_lock(&op_mutex);
	arg_v[0] = arg1;
	arg_v[1] = arg2;
	arg_v[2] = arg3;
	arg_n = n;
	arg_c = c;
	arg_op = op;
	op_count = 0;
	for(op_count = 0; op_count < THREAD_NUMBER; op_count++)
	{
		pthread_mutex_lock(&mutex[op_count]);
		pthread_cond_signal(&cond[op_count]);
		pthread_mutex_unlock(&mutex[op_count]);
	}
	while(op_count)
		pthread_cond_wait(&op_cond, &op_mutex);
	pthread_mutex_unlock(&op_mutex);
}

inline static void vecset(lbfgsfloatval_t *x, const lbfgsfloatval_t c, const int n)
{
	submit_thread(x, NULL, NULL, c, n, VECSET);
}

inline static void veccpy(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const int n)
{
	memcpy(y, x, sizeof(lbfgsfloatval_t) * n);
}

inline static void vecncpy(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const int n)
{
	submit_thread(y, x, NULL, 0, n, VECNCPY);
}

inline static void vecadd(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const lbfgsfloatval_t c, const int n)
{
	submit_thread(y, x, NULL, c, n, VECADD);
}

inline static void vecdiff(lbfgsfloatval_t *z, const lbfgsfloatval_t *x, const lbfgsfloatval_t *y, const int n)
{
	submit_thread(z, x, y, 0, n, VECDIFF);
}

inline static void vecscale(lbfgsfloatval_t *y, const lbfgsfloatval_t c, const int n)
{
	submit_thread(y, NULL, NULL, c, n, VECSCALE);
}

inline static void vecmul(lbfgsfloatval_t *y, const lbfgsfloatval_t *x, const int n)
{
	submit_thread(y, x, NULL, 0, n, VECMUL);
}

inline static void vecdot(lbfgsfloatval_t* s, const lbfgsfloatval_t *x, const lbfgsfloatval_t *y, const int n)
{
	int i;
	*s = 0.;
	submit_thread(x, y, NULL, 0, n, VECDOT);
	for(i = 0; i < THREAD_NUMBER; i++)
		*s += temp_dot[i];
}

inline static void vec2norm(lbfgsfloatval_t* s, const lbfgsfloatval_t *x, const int n)
{
    vecdot(s, x, x, n);
    *s = (lbfgsfloatval_t)sqrt(*s);
}

inline static void vec2norminv(lbfgsfloatval_t* s, const lbfgsfloatval_t *x, const int n)
{
    vec2norm(s, x, n);
    *s = (lbfgsfloatval_t)(1.0 / *s);
}

void *thread_common(void *arg)
{
	int index = (int)arg;
	do {
		pthread_mutex_lock(&mutex[index]);
		pthread_cond_wait(&cond[index], &mutex[index]);
		pthread_mutex_unlock(&mutex[index]);

		switch(arg_op)
		{
			int n, i;
			lbfgsfloatval_t s, c, *x, *y, *z;
			case VECSET:
				x = arg_v[0];
				c = arg_c;
				n = arg_n;

				for (i = index; i < n; i += THREAD_NUMBER) {
					x[i] = c;
				}
				break;

			case VECNCPY:
				y = arg_v[0];
				x = arg_v[1];
				n = arg_n;

				for (i = index; i < n; i += THREAD_NUMBER) {
					y[i] = -x[i];
				}
				break;

			case VECADD:
				y = arg_v[0];
				x = arg_v[1];
				c = arg_c;
				n = arg_n;
				for (i = index; i < n; i += THREAD_NUMBER) {
					y[i] += c * x[i];
				}
				break;

			case VECDIFF:
				z = arg_v[0];
				x = arg_v[1];
				y = arg_v[2];
				n = arg_n;
				for (i = index; i < n; i += THREAD_NUMBER) {
					z[i] = x[i] - y[i];
				}
				break;

			case VECSCALE:
				y = arg_v[0];
				c = arg_c;
				n = arg_n;
				for (i = index; i < n; i += THREAD_NUMBER) {
					y[i] *= c;
				}
				break;

			case VECMUL:
				y = arg_v[0];
				x = arg_v[1];
				n = arg_n;
				for (i = index; i < n; i += THREAD_NUMBER) {
					y[i] *= x[i];
				}
				break;

			case VECDOT:
				x = arg_v[0];
				y = arg_v[1];
				s = 0.;
				n = arg_n;
				for (i = index; i < n; i += THREAD_NUMBER) {
					s += x[i] * y[i];
				}
				temp_dot[index] = s;
				break;

			default:
				break;
		}
		pthread_mutex_lock(&op_mutex);
		op_count--;
		pthread_cond_signal(&op_cond);
		pthread_mutex_unlock(&op_mutex);

	} while(1);
	return NULL;
}

void ansi_init(void)
{
	if(first == 1)
	{
		int i;
		first = 0;
		pthread_mutex_init(&op_mutex, NULL);
		pthread_cond_init(&op_cond, NULL);
		for(i = 0; i < THREAD_NUMBER; i++)
		{
			pthread_mutex_init(&mutex[i], NULL);
			pthread_cond_init(&cond[i], NULL);
			pthread_create(&pid_thread[i], NULL, (void *)thread_common, (void *)i);
		}
	}
}
#endif
