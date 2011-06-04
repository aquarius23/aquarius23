/*	
	ida.c	
	This module provides basic functionality for Information Dispersal Algorithm.
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
#include "matrix.h"
#include "ida.h"

static struct gf2_matrix *alloc_matrix(int w, int n, int m)
{
	struct gf2_matrix *matrix =  alloc_empty_matrix(w, n, m);
	if(!matrix)
		return NULL;
	matrix->values = malloc(w * n * m);
	if(!matrix->values)
	{
		free_matrix(matrix);
		return NULL;
	}
	return matrix;
}

struct ida_data *create_ida(int width, int n, int m)
{
	struct ida_data *ret;
	if(n < m)
		return NULL;
	if((width != 1) && (width != 2))
		return NULL;
	ret = malloc(sizeof(struct ida_data));
	if(!ret)
		return NULL;

	ret->key = generate_cauchy_matrix(width, n, m);
	if(!ret->key)
	{
		free(ret);
		return NULL;
	}
	ret->split = alloc_matrix(width, n, m);
	if(!ret->split)
	{
		free_matrix(ret->key);
		free(ret);
		return NULL;
	}
	ret->encode = alloc_empty_matrix(width, m, m);
	if(!ret->encode)
	{
		free_matrix(ret->split);
		free_matrix(ret->key);
		free(ret);
		return NULL;
	}
	ret->decode = alloc_empty_matrix(width, m, m);
	if(!ret->decode)
	{
		free_matrix(ret->encode);
		free_matrix(ret->split);
		free_matrix(ret->key);
		free(ret);
		return NULL;
	}
	ret->reverse = NULL;
	ret->width = width;
	ret->n = n;
	ret->m = m;
	ret->size = width * m * m;
	return ret;
}

int get_ida_block_size(struct ida_data *ida)
{
	return ida->size;
}

void free_ida(struct ida_data *ida)
{
	free_matrix(ida->key);
	free_matrix(ida->split);
	ida->encode->values = NULL;
	free_matrix(ida->encode);
	ida->decode->values = NULL;
	free_matrix(ida->decode);
	if(ida->reverse)
		free_matrix(ida->reverse);
	free(ida);
}

static char *get_matrix_vector(struct gf2_matrix *matrix, int index, int *size)
{
	int length;
	if(!matrix)
		return NULL;
	if(index >= matrix->rows)	// index = 0, 1, ... ROWS-1
		return NULL;
	length = matrix->cols * matrix->width;
	if(size)
		*size = length;
	return (char *)(matrix->values + index * length);
}

char *get_key_vector(struct ida_data *ida, int index, int *size)
{
	return get_matrix_vector(ida->key, index, size);
}

char *get_split_vector(struct ida_data *ida, int index, int *size)
{
	return get_matrix_vector(ida->split, index, size);
}

int set_combine_matrix(struct ida_data *ida, void *input)
{
	struct gf2_matrix matrix;
	matrix.width = ida->width;
	matrix.rows = ida->m;
	matrix.cols = ida->m;
	matrix.values = input;
	if(ida->reverse)
	{
		free_matrix(ida->reverse);
		ida->reverse = NULL;
	}
	ida->reverse = revert_matrix(&matrix);
	if(!ida->reverse)
		return -1;
	return 0;
}

void encode_data(struct ida_data *ida, void *input)
{
	ida->encode->values = input;
	multiply_matrix(ida->key, ida->encode, ida->split);
}

void decode_data(struct ida_data *ida, void *input, void *output)
{
	ida->encode->values = input;
	ida->decode->values = output;
	multiply_matrix(ida->reverse, ida->encode, ida->decode);
}

struct gf2_matrix *set_another_combine_matrix(struct ida_data *ida, void *input)
{
	struct gf2_matrix matrix, *ret;
	matrix.width = ida->width;
	matrix.rows = ida->m;
	matrix.cols = ida->m;
	matrix.values = input;
	ret = revert_matrix(&matrix);
	if(!ret)
		return NULL;
	return ret;
}

void another_decode_data(struct ida_data *ida, struct gf2_matrix *matrix, void *input, void *output)
{
	struct gf2_matrix matrix_in, matrix_out;
	matrix_in.width = ida->width;
	matrix_in.rows = ida->m;
	matrix_in.cols = ida->m;
	matrix_in.values = input;

	matrix_out.width = ida->width;
	matrix_out.rows = ida->m;
	matrix_out.cols = ida->m;
	matrix_out.values = output;
	multiply_matrix(matrix, &matrix_in, &matrix_out);
}

void free_another_matrix(struct gf2_matrix *matrix)
{
	free_matrix(matrix);
}
