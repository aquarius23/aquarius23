#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int g_y[800*480];
int g_u[800*480];
int g_v[800*480];

struct dwt_resolution {
	int x0, y0, x1, y1;
};

struct dwt_local
{
	int* mem;
	int dn;
	int sn;
	int cas;
};

/* <summary>                             */
/* Forward lazy transform (horizontal).  */
/* </summary>                            */
static void dwt_deinterleave_h(int *a, int *b, int dn, int sn, int cas) {
    int i;
    for (i=0; i<sn; i++) b[i]=a[2*i+cas];
    for (i=0; i<dn; i++) b[sn+i]=a[(2*i+1-cas)];
}

/* <summary>                             */
/* Forward lazy transform (vertical).    */
/* </summary>                            */
static void dwt_deinterleave_v(int *a, int *b, int dn, int sn, int x, int cas) {
    int i;
    for (i=0; i<sn; i++) b[i*x]=a[2*i+cas];
    for (i=0; i<dn; i++) b[(sn+i)*x]=a[(2*i+1-cas)];
}

/* <summary>                             */
/* Inverse lazy transform (horizontal).  */
/* </summary>                            */
static void dwt_interleave_h(struct dwt_local* h, int *a) {
	int *ai = a;
	int *bi = h->mem + h->cas;
	int i = h->sn;
	while( i-- )
	{
		*bi = *(ai++);
		bi += 2;
	}
	ai = a + h->sn;
	bi = h->mem + 1 - h->cas;
	i = h->dn ;
	while( i-- )
	{
		*bi = *(ai++);
		bi += 2;
	}
}

/* <summary>                             */
/* Inverse lazy transform (vertical).    */
/* </summary>                            */
static void dwt_interleave_v(struct dwt_local* v, int *a, int x) {
	int *ai = a;
	int *bi = v->mem + v->cas;
	int  i = v->sn;
	while(i--)
	{
		*bi = *ai;
		bi += 2;
		ai += x;
	}
	ai = a + (v->sn * x);
	bi = v->mem + 1 - v->cas;
	i = v->dn ;
	while(i--)
	{
		*bi = *ai;
		bi += 2;
		ai += x;
	}
}

#define S(i) a[(i)*2]
#define D(i) a[(1+(i)*2)]
#define S_(i) ((i)<0?S(0):((i)>=sn?S(sn-1):S(i)))
#define D_(i) ((i)<0?D(0):((i)>=dn?D(dn-1):D(i)))
#define SS_(i) ((i)<0?S(0):((i)>=dn?S(dn-1):S(i)))
#define DD_(i) ((i)<0?D(0):((i)>=sn?D(sn-1):D(i)))

/* <summary>                            */
/* Forward 5-3 wavelet transform in 1-D. */
/* </summary>                           */
static void dwt_encode_1(int *a, int dn, int sn, int cas) {
    int i;

    if (!cas) {
        if ((dn > 0) || (sn > 1)) { /* NEW :  CASE ONE ELEMENT */
            for (i = 0; i < dn; i++) D(i) -= (S_(i) + S_(i + 1)) >> 1;
            for (i = 0; i < sn; i++) S(i) += (D_(i - 1) + D_(i) + 2) >> 2;
        }
    } else {
        if (!sn && dn == 1)         /* NEW :  CASE ONE ELEMENT */
            S(0) *= 2;
        else {
            for (i = 0; i < dn; i++) S(i) -= (DD_(i) + DD_(i - 1)) >> 1;
            for (i = 0; i < sn; i++) D(i) += (SS_(i) + SS_(i + 1) + 2) >> 2;
        }
    }
}

/* <summary>                            */
/* Inverse 5-3 wavelet transform in 1-D. */
/* </summary>                           */
static void dwt_decode_1(int *a, int dn, int sn, int cas) {
    int i;

    if (!cas) {
        if ((dn > 0) || (sn > 1)) { /* NEW :  CASE ONE ELEMENT */
            for (i = 0; i < sn; i++) S(i) -= (D_(i - 1) + D_(i) + 2) >> 2;
            for (i = 0; i < dn; i++) D(i) += (S_(i) + S_(i + 1)) >> 1;
        }
    } else {
        if (!sn  && dn == 1)          /* NEW :  CASE ONE ELEMENT */
            S(0) /= 2;
        else {
            for (i = 0; i < sn; i++) D(i) -= (SS_(i) + SS_(i + 1) + 2) >> 2;
            for (i = 0; i < dn; i++) S(i) += (DD_(i) + DD_(i - 1)) >> 1;
        }
    }
}

struct dwt_resolution *alloc_resolution(int num, int width, int height)
{
	struct dwt_resolution *l_cur_res;
	struct dwt_resolution *ret = malloc(sizeof(struct dwt_resolution) * (num + 1));
	if(!ret)
		return NULL;
	l_cur_res = ret + num;
	l_cur_res->x0 = 0;
	l_cur_res->y0 = 0;
	l_cur_res->x1 = width;
	l_cur_res->y1 = height;
	while(num--)
	{
		l_cur_res--;
		l_cur_res->x0 = 0;
		l_cur_res->y0 = 0;
		l_cur_res->x1 = ((l_cur_res + 1)->x1 + 1) >> 1;
		l_cur_res->y1 = ((l_cur_res + 1)->y1 + 1) >> 1;
	};
	return ret;
}

void free_resolution(struct dwt_resolution * resolution)
{
	free(resolution);
}

int dwt_encode(int *a, int width, int height)
{
	int *aj, *bj;
	int rw, rh, rw1, rh1, dn, sn, cas_row, cas_col;
	int l_data_size = (width < height) ? height: width;
	int i, j, k;
	int w = width;
	struct dwt_resolution *resolution, *l_cur_res, *l_last_res;

	i = 5;
	resolution = alloc_resolution(i, width, height);
	bj = malloc(l_data_size * sizeof(int));
	if(!bj)
	{
		free_resolution(resolution);
		return -1;
	}

	l_cur_res = resolution + i;
	l_last_res = l_cur_res - 1;

	while(i--)
	{
		rw  = l_cur_res->x1 - l_cur_res->x0;
		rh  = l_cur_res->y1 - l_cur_res->y0;
		rw1 = l_last_res->x1 - l_last_res->x0;
		rh1 = l_last_res->y1 - l_last_res->y0;
		cas_row = l_cur_res->x0 & 1;
		cas_col = l_cur_res->y0 & 1;

		sn = rh1;
		dn = rh - rh1;
		for(j = 0; j < rw; ++j)
		{
			aj = a + j;
			for(k = 0; k < rh; ++k)
				bj[k] = aj[k*w];
			dwt_encode_1 (bj, dn, sn, cas_col);
			dwt_deinterleave_v(bj, aj, dn, sn, w, cas_col);
		}

		sn = rw1;
		dn = rw - rw1;
		for (j = 0; j < rh; j++)
		{
			aj = a + j * w;
			for (k = 0; k < rw; k++)
				bj[k] = aj[k];
			dwt_encode_1 (bj, dn, sn, cas_row);
			dwt_deinterleave_h(bj, aj, dn, sn, cas_row);
		}

		l_cur_res = l_last_res;
		--l_last_res;
	}
	free(bj);
	free_resolution(resolution);
	return 0;
}

int dwt_decode(int *a, int width, int height)
{
	struct dwt_local h, v;
	int i = 5;
	struct dwt_resolution *temp;
	struct dwt_resolution *tr = alloc_resolution(5, width, height);
	temp = tr;
	int l_data_size = (width < height) ? height: width;
	int rw = tr->x1 - tr->x0;	/* width of the resolution level computed */
	int rh = tr->y1 - tr->y0;	/* height of the resolution level computed */
	int w = width;

	h.mem = malloc(l_data_size * sizeof(int));
	if(!h.mem)
	{
		free_resolution(tr);
		return -1;
	}

	v.mem = h.mem;
	while(i--) {
		int *tiledp = a;
		int j;

		++tr;
		h.sn = rw;
		v.sn = rh;

		rw = tr->x1 - tr->x0;
		rh = tr->y1 - tr->y0;

		h.dn = rw - h.sn;
		h.cas = tr->x0 % 2;

		for(j = 0; j < rh; ++j) {
			dwt_interleave_h(&h, &tiledp[j*w]);
			dwt_decode_1(h.mem, h.dn, h.sn, h.cas);
			memcpy(&tiledp[j*w], h.mem, rw * sizeof(int));
		}

		v.dn = rh - v.sn;
		v.cas = tr->y0 % 2;

		for(j = 0; j < rw; ++j){
			int k;
			dwt_interleave_v(&v, &tiledp[j], w);
			dwt_decode_1(v.mem, v.dn, v.sn, v.cas);
			for(k = 0; k < rh; ++k)
				tiledp[k * w + j] = v.mem[k];
		}
	}
	free(h.mem);
	free_resolution(temp);
	return 0;
}

void rgb2yuv(char *p)
{
	int i;
	int r, g, b;
	int y, u, v;
	for(i = 0; i < 800*480; i++)
	{
		r = p[i*3];
		g = p[i*3 + 1];
		b = p[i*3 + 2];

		y = (r + (g * 2) + b) >> 2;
		u = b - g;
		v = r - g;

		g_y[i] = y;
		g_u[i] = u;
		g_v[i] = v;
	}
}

void yuv2rgb(char *p)
{
	int i;
	int r, g, b;
	int y, u, v;
	for(i = 0; i < 800*480; i++)
	{
		y = g_y[i];
		u = g_u[i];
		v = g_v[i];

		g = y - ((u + v) >> 2);
		r = v + g;
		b = u + g;

		p[i*3] = r;
		p[i*3 + 1] = g;
		p[i*3 + 2] = b;
	}
}

void test_wavelet(char *p, int size)
{
	rgb2yuv(p);
	dwt_encode(g_y, 480, 800);
	dwt_encode(g_u, 480, 800);
	dwt_encode(g_v, 480, 800);

//	memset(g_y + 480*400, 0 ,480*400*4);
//	memset(g_u + 480*400, 0 ,480*400*4);
//	memset(g_v + 480*400, 0 ,480*400*4);

	dwt_decode(g_y, 480, 800);
	dwt_decode(g_u, 480, 800);
	dwt_decode(g_v, 480, 800);

	yuv2rgb(p);
}

