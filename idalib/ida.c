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
#include <memory.h>
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

struct ida_encode *ida_encode_create(int width, int n, int m)
{
	struct ida_encode *ret;
	if(n < m)
		return NULL;
	if((width != 1) && (width != 2))
		return NULL;
	ret = malloc(sizeof(struct ida_encode));
	if(!ret)
		return NULL;

	memset(ret, 0, sizeof(struct ida_encode));
	ret->key = generate_cauchy_matrix(width, n, m);
	if(!ret->key)
	{
		free(ret);
		return NULL;
	}
	ret->input = alloc_empty_matrix(width, m, m);
	if(!ret->input)
	{
		free_matrix(ret->key);
		free(ret);
		return NULL;
	}
	ret->output = alloc_matrix(width, n, m);
	if(!ret->output)
	{
		free_matrix2(ret->input);
		free_matrix(ret->key);
		free(ret);
		return NULL;
	}
	ret->width = width;
	ret->n = n;
	ret->m = m;
	ret->size = width * n * m;
	return ret;
}

void ida_encode_free(struct ida_encode *ida)
{
	if(!ida)
		return;
	free_matrix(ida->key);
	free_matrix(ida->output);
	free_matrix2(ida->input);
	free(ida);
}

int ida_encode_block_size(struct ida_encode *ida)
{
	if(!ida)
		return 0;
	return ida->width * ida->m * ida->m;
}

int ida_encode_data(struct ida_encode *ida, void *input)
{
	if(!ida || !input)
		return 0;
	ida->input->values = input;
	multiply_matrix(ida->key, ida->input, ida->output);
	return ida->width * ida->m * ida->m;
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

char *ida_encode_key_vector(struct ida_encode *ida, int index, int *size)
{
	return get_matrix_vector(ida->key, index, size);
}

char *ida_encode_output_vector(struct ida_encode *ida, int index, int *size)
{
	return get_matrix_vector(ida->output, index, size);
}

struct ida_decode *ida_decode_create(int width, int m)
{
	struct ida_decode *ret;
	if((width != 1) && (width != 2))
		return NULL;
	ret = malloc(sizeof(struct ida_decode));
	if(!ret)
		return NULL;

	memset(ret, 0, sizeof(struct ida_decode));
	ret->input = alloc_empty_matrix(width, m, m);
	if(!ret->input)
	{
		free(ret);
		return NULL;
	}
	ret->output = alloc_empty_matrix(width, m, m);
	if(!ret->output)
	{
		free_matrix2(ret->input);
		free(ret);
		return NULL;
	}
	ret->width = width;
	ret->m = m;
	ret->size = width * m * m;
	return ret;
}

void ida_decode_free(struct ida_decode *ida)
{
	if(!ida)
		return;
	if(ida->key)
		free_matrix(ida->key);
	free_matrix2(ida->output);
	free_matrix2(ida->input);
	free(ida);
}


int ida_decode_set_key(struct ida_decode *ida, void *input)
{
	struct gf2_matrix matrix;
	if(!ida || !input)
		return 0;
	matrix.width = ida->width;
	matrix.rows = ida->m;
	matrix.cols = ida->m;
	matrix.values = input;
	ida->key = revert_matrix(&matrix);
	if(!ida->key)
		return 0;
	return 1;
}

int ida_decode_data(struct ida_decode *ida, void *input, void *output)
{
	if(!ida || !input || !output)
		return 0;
	ida->input->values = input;
	ida->output->values = output;
	multiply_matrix(ida->key, ida->input, ida->output);
	return ida->width * ida->m * ida->m;
}

