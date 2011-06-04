/*	
	matrix.c	
	This module provides basic functionality for handling matrices of Galois Field elements.
	Copyright (C) 2009 Haibo Hu <aquarius23@126.com> & <haibo.hu@archermind.com>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gf2.h"
#include "matrix.h"	

//#define MULTIPLY_MATRIX_CHECK		1

static unsigned short read_w16(unsigned char *buf)
{
	return *buf | (*(buf + 1) << 8);
}

static void write_w16(unsigned char *buf, unsigned short val)
{
	*buf++ = val & 0xff;
	*buf = (val >> 8) & 0xff;
}

static int generate_random()
{
	return rand();
}

static struct key_list *generate_key_list(int w, int n, int m)
{
	int i, j, mask;
	struct key_list *ret = NULL;

	switch(w)
	{
	case 1:
		mask = 0xff;
		break;

	case 2:
		mask = 0xffff;
		break;

	case 4:
		mask =  0xffffffff;
		break;

	default:
		return NULL;
	}

	ret = malloc(sizeof(struct key_list)); 
	if(!ret)
		return NULL;
	ret->width = w;
	ret->values = malloc((n + m) * sizeof(int));
	if(!ret->values)
	{
		free(ret);
		return NULL;
	}

	for(i = 0; i < (n + m); i++) 
	{
		int random;
		do
		{
			random = generate_random();
			random &= mask;
			if(random == 0)
				continue;
			for(j = 0; j < i; j++)
			{
				if(ret->values[j] == random)
					break;
			}
			if(j >= i)
				break;
		} while(1);
		ret->values[i] = random;
	}
	return ret;
}

static void free_key_list(struct key_list *list)
{
	free(list->values);
	free(list);
}

struct gf2_matrix *alloc_empty_matrix(int w, int n, int m)
{
	struct gf2_matrix *ret = NULL;
	if((w != 1) && (w != 2))
		return NULL;

	ret = malloc(sizeof(struct gf2_matrix));
	if(!ret)
		return NULL;
	ret->values = NULL;
	ret->width = w;
	ret->rows = n;
	ret->cols = m;
	return ret;
}

struct gf2_matrix *generate_cauchy_matrix(int w, int n, int m)
{
	int i, j, sum;
	struct gf2_matrix *ret = NULL;
	struct key_list *list = NULL;
	if((w != 1) && (w != 2))
		return NULL;

	list = generate_key_list(w, n, m);
	if(!list)
		return NULL;

	ret = malloc(sizeof(struct gf2_matrix));
	if(!ret)
	{
		free_key_list(list);
		return NULL;
	}
	ret->values = malloc(n * m * w);
	if(!ret->values)
	{
		free(ret);
		free_key_list(list);
		return NULL;
	}
	ret->width = w;
	ret->rows = n;
	ret->cols = m;

	for(i = 0; i < n; i++)
		for(j = 0; j < m; j++)
		{
			sum = list->values[i] ^ list->values[n + j];
			if(w == 1)
			{			
				ret->values[i * ret->cols + j] = galois_divide_w8(1, sum & 0xff);
			}
			else if(w == 2)
			{	
				write_w16(ret->values + (i * ret->cols + j) * 2, galois_divide_w16(1, sum & 0xffff));
			}
		}

	free_key_list(list);
	return ret;
}

void free_matrix(struct gf2_matrix *matrix)
{
	if(matrix->values)
		free(matrix->values);
	free(matrix);
}

struct gf2_matrix *revert_matrix(struct gf2_matrix * matrix)	/* Gauss-Jordan method */
{
	int i, j, k;
	struct gf2_matrix *reverse, *temp = NULL;
	if(!matrix)
		return NULL;
	if(matrix->rows != matrix->cols)
		return NULL;
	if((matrix->width != 1) && (matrix->width != 2))
		return NULL;

	reverse = malloc(sizeof(struct gf2_matrix));
	if(!reverse)
		return NULL;
	reverse->values = malloc(matrix->rows * matrix->cols * matrix->width);
	if(!reverse->values)
	{
		free(reverse);
		return NULL;
	}

	temp = malloc(sizeof(struct gf2_matrix));
	if(!temp)
	{
		free_matrix(reverse);
		return NULL;
	}
	temp->values = malloc(matrix->rows * matrix->cols * matrix->width * 2);
	memset(temp->values, 0, matrix->rows * matrix->cols * matrix->width * 2);
	if(!temp->values)
	{
		free_matrix(reverse);
		free(temp);
		return NULL;
	}

	temp->width = matrix->width;
	temp->rows = matrix->rows;
	temp->cols = matrix->cols * 2;

	for(i = 0; i < matrix->rows; i++)
		for(j = 0; j < matrix->cols; j++)
		{
			if(matrix->width == 1)
			{
				temp->values[i * temp->cols + j] = matrix->values[i * matrix->cols + j];
			}
			else if(matrix->width == 2)
			{
				unsigned short element = read_w16(matrix->values + (i * matrix->cols + j) * 2);
				write_w16(temp->values + (i * temp->cols + j) * 2, element);
			}
		}

	for(i = 0; i < matrix->rows; i++)
	{
		if(matrix->width == 1)
		{
			temp->values[i * temp->cols + matrix->cols + i] = 1;
		}
		else if(matrix ->width == 2)
		{
			write_w16(temp->values + (i * temp->cols + matrix->cols + i) * 2, 1);
		}
	}

/*********** Gauss-Jordan method ************/
	
	switch(temp->width)
	{
	case 1:
		for(i = 0; i < temp->rows; i++)
		{
			unsigned char reverse_w8, element;
			if(temp->values[i * temp->cols + i] == 0)
			{
				int x, y;
				for(x = i + 1; x < temp->rows; x++)
				{
					if(temp->values[x * temp->cols + i] != 0)
						break;
				}
				if(x >= temp->rows)
				{
					free_matrix(temp);
					free_matrix(reverse);
					return NULL;
				}
				for(y = i; y < temp->cols; y++)	/* swap rows */
				{
					element = temp->values[i * temp->cols + y];
					temp->values[i * temp->cols + y] = temp->values[x * temp->cols + y];
					temp->values[x * temp->cols + y] = element;
				}
			}

			reverse_w8 = galois_divide_w8(1, temp->values[i * temp->cols + i]);
			temp->values[i * temp->cols + i] = 1;
			for(j = i + 1; j < temp->cols; j++)
			{
				element = galois_multiply_w8(temp->values[i * temp->cols + j], reverse_w8);
				temp->values[i * temp->cols + j] = element;
			}

			/* zero all elements above and below ... */
			for(j = 0; j < temp->rows; j++)
			{
				if(j == i)
					continue;
				reverse_w8 = temp->values[j * temp->cols + i];
				if(reverse == 0)
					continue;
				temp->values[j * temp->cols + i] = 0;
				for(k = i + 1; k < temp->cols; k++)
				{
					element = galois_multiply_w8(temp->values[i * temp->cols + k], reverse_w8);
					temp->values[j * temp->cols + k] ^= element;
				}
			}
		}
		break;

	case 2:
		for(i = 0; i < temp->rows; i++)
		{
			unsigned short reverse_w16, element;
			if(read_w16(temp->values + (i * temp->cols + i) * 2) == 0)
			{
				int x, y;
				for(x = i + 1; x < temp->rows; x++)
				{
					if(read_w16(temp->values + (x * temp->cols + i) * 2) != 0)
						break;
				}
				if(x >= temp->rows)
				{
					free_matrix(temp);
					free_matrix(reverse);
					return NULL;
				}
				for(y = i; y < temp->cols; y++)	/* swap rows */
				{
					element = read_w16(temp->values + (i * temp->cols + y) * 2);
					write_w16(temp->values + (i * temp->cols + y) * 2, read_w16(temp->values + (x * temp->cols + y) * 2));
					write_w16(temp->values + (x * temp->cols + y) * 2, element);
				}
			}

			reverse_w16 = galois_divide_w16(1, read_w16(temp->values + (i * temp->cols + i) * 2));
			write_w16(temp->values + (i * temp->cols + i) * 2, 1);
			for(j = i + 1; j < temp->cols; j++)
			{
				element = galois_multiply_w16(read_w16(temp->values + (i * temp->cols + j) * 2), reverse_w16);
				write_w16(temp->values + (i * temp->cols + j) * 2, element);
			}

			/* zero all elements above and below ... */
			for(j = 0; j < temp->rows; j++)
			{
				if(j == i)
					continue;
				reverse_w16 = read_w16(temp->values + (j * temp->cols + i) * 2);
				if(reverse == 0)
					continue;
				write_w16(temp->values + (j * temp->cols + i) * 2, 0);
				for(k = i + 1; k < temp->cols; k++)
				{
					element = galois_multiply_w16(read_w16(temp->values + (i * temp->cols + k) * 2), reverse_w16);
					write_w16(temp->values + (j * temp->cols + k) * 2, read_w16(temp->values + (j * temp->cols + k) * 2) ^ element);
				}
			}
		}
		break;

	default:
		break;
	}
	
	/* save reverse matrix */
	reverse->width = matrix->width;
	reverse->rows = matrix->rows;
	reverse->cols = matrix->cols;
	for(i = 0; i < reverse->rows; i++)
		for(j = 0; j < reverse->cols; j++)
		{
			if(reverse->width == 1)
			{
				reverse->values[i * reverse->cols + j] = temp->values[i * temp->cols + reverse->cols + j];
			}
			else if(reverse->width == 2)
			{
				unsigned short element = read_w16(temp->values + (i * temp->cols + reverse->cols + j) * 2);
				write_w16(reverse->values + (i * reverse->cols + j) * 2, element);
			}
		}
	free_matrix(temp);
	return reverse;
}

int multiply_matrix(struct gf2_matrix *a, struct gf2_matrix *b, struct gf2_matrix *c)	// c = a * b
{
	int i, j, k;
	unsigned char *a_w8, *b_w8, *c_w8, element_w8;
	unsigned short *a_w16, *b_w16, *c_w16, element_w16;

	if(!a && !b && !c)
		return -1;

#ifdef MULTIPLY_MATRIX_CHECK
	if((a->width != b->width) || (b->width != c->width))
		return -1;
	if(a->cols != b->rows)
		return -1;
	if((a->rows != c->rows) || (b->cols != c->cols))
		return -1;
#endif

	switch(a->width)
	{
	case 1:
		c_w8 = c->values;
		for(i = 0; i < a->rows; i++)
		{
			for(j = 0; j < b->cols; j++)
			{
				element_w8 = 0;
				a_w8 = a->values + i * a->cols * sizeof(unsigned char);
				b_w8 = b->values + j * sizeof(unsigned char);
				for(k = 0; k < a->cols; k++)
				{
					element_w8 ^= galois_multiply_w8(*a_w8, *b_w8);
					a_w8++;
					b_w8 += b->cols;
				}
				*c_w8++ = element_w8;
			}
		}
		break;

	case 2:
		c_w16 = (unsigned short *)c->values;
		for(i = 0; i < a->rows; i++)
		{
			for(j = 0; j < b->cols; j++)
			{
				element_w16 = 0;
				a_w16 = (unsigned short *)(a->values + i * a->cols * sizeof(unsigned short));
				b_w16 = (unsigned short *)(b->values + j * sizeof(unsigned short));
				for(k = 0; k < a->cols; k++)
				{
					element_w16 ^= galois_multiply_w16(read_w16((unsigned char *)a_w16), read_w16((unsigned char *)b_w16));
					a_w16++;
					b_w16 += b->cols;
				}
				write_w16((unsigned char *)c_w16, element_w16);
				c_w16++;
			}
		}
		break;

	default:
		return -1;
	}

	return 0;
}
