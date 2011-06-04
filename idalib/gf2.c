/*	
	gf2.c	Galois Field arithmetic
	Copyright (C) 2009 Haibo Hu <aquarius23@126.com> & <haibo.hu@archermind.com>
	
	Primitive Polynomials:
	GF(2^8)		x^8 + x^4 + x^3 + x^2 + 1
	GF(2^16)	x^16 + x^12 + x^3 + x + 1

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
#include "gf2.h"

const static int prim_poly_8 = 0x11d;	/* x^8 + x^4 + x^3 + x^2 + 1 */
const static int prim_poly_16 = 0x1100b;	/* x^16 + x^12 + x^3 + x + 1 */

static int gf2_flag_8 = 0;
static int gf2_flag_16 = 0;

static struct gf2_table gf2_table_8 = {0,NULL,NULL,NULL}, gf2_table_16 = {0,NULL,NULL,NULL}; 

int galois_field_create_tables(int index, struct gf2_table *table)
{
	int i, j, size, prim_poly;
	
	if(!table)
		return -1;

	table->index = index;
	size = (1 << index) * sizeof(unsigned short);
	if(index == GF2_INDEX_8)
		prim_poly = prim_poly_8;
	else if(index == GF2_INDEX_16)
		prim_poly = prim_poly_16;
	else
		return -1;

	table->log = malloc(size);
	if(!table->log)
		return -1;
	table->exp = malloc(size);
	if(!table->exp)
	{
		free(table->log);
		table->log = NULL;
		return -1;
	}
	if(index == GF2_INDEX_8)
	{
		table->mult = malloc((1 << GF2_INDEX_8) * (1 << GF2_INDEX_8));
		if(!table->mult)
		{
			free(table->log);
			free(table->exp);
			table->log = NULL;
			table->exp = NULL;
			return -1;
		}
		table->div = malloc((1 << GF2_INDEX_8) * (1 << GF2_INDEX_8));
		if(!table->div)
		{
			free(table->log);
			free(table->exp);
			free(table->mult);
			table->log = NULL;
			table->exp = NULL;
			table->mult = NULL;
			return -1;
		}
	}

	for(i = 0, j = 1; i < (1 << index); i++)
	{
		table->log[j] = (unsigned short)i;
		table->exp[i] = (unsigned short)j;
		j = j << 1;			// polynomials * x
		if(j & (1 << index))
			j = j ^ prim_poly;	// polynomials mod prim_poly
	}
	table->log[1] = 0;

	if(table->mult)
	{
		unsigned short x, y, p, q, logx, logy;

		for(x = 0; x < (1 << GF2_INDEX_8); x++)
		{
			for(y = 0; y < (1 << GF2_INDEX_8); y++)
			{
				i = (x << GF2_INDEX_8) | y;
				if(y == 0)
				{
					table->mult[i] = 0;
					table->div[i] = 0xff;
					continue;
				}
				if(x == 0)
				{
					table->mult[i] = 0;
					table->div[i] = 0;
					continue;
				}

				logx = table->log[x];
				logy = table->log[y];

				p = logx + logy;
				if(p >= ((1 << GF2_INDEX_8) - 1))
					p -= (1 << GF2_INDEX_8) - 1;

				if(logx < logy)
					logx += (1 << GF2_INDEX_8) - 1;
				q = logx - logy;

				table->mult[i] = table->exp[p] & ((1 << GF2_INDEX_8) - 1); 
				table->div[i] = table->exp[q] & ((1 << GF2_INDEX_8) - 1); 
			}
		}
	}
	return 0;
}

unsigned char galois_multiply_w8(unsigned char x, unsigned char y)
{
	if(!gf2_flag_8)
	{
		galois_field_create_tables(GF2_INDEX_8, &gf2_table_8);
		gf2_flag_8 = 1;
	}
	return gf2_table_8.mult[(x << GF2_INDEX_8) | y];
}

unsigned char galois_divide_w8(unsigned char x, unsigned char y)
{
	if(!gf2_flag_8)
	{
		galois_field_create_tables(GF2_INDEX_8, &gf2_table_8);
		gf2_flag_8 = 1;
	}
	return gf2_table_8.div[(x << GF2_INDEX_8) | y];
}

unsigned short galois_multiply_w16(unsigned short x, unsigned short y)
{
	unsigned int p;
	unsigned short logx, logy;

	if(x == 0 || y == 0)
		return 0;

	if(!gf2_flag_16)
	{
		galois_field_create_tables(GF2_INDEX_16, &gf2_table_16);
		gf2_flag_16 = 1;
	}

	logx = gf2_table_16.log[x];
	logy = gf2_table_16.log[y];

	p = logx + logy;
	if(p >= ((1 << GF2_INDEX_16) - 1))
		p -= (1 << GF2_INDEX_16) - 1;

	return gf2_table_16.exp[p];
}

unsigned short galois_divide_w16(unsigned short x, unsigned short y)
{
	unsigned int q;
	unsigned short logx, logy;

	if(y == 0)
		return 0xffff;
	if(x == 0)
		return 0; 

	if(!gf2_flag_16)
	{
		galois_field_create_tables(GF2_INDEX_16, &gf2_table_16);
		gf2_flag_16 = 1;
	}

	logx = gf2_table_16.log[x];
	logy = gf2_table_16.log[y];

	q = logx;
	if(q < logy)
		q += (1 << GF2_INDEX_16) - 1;
	q -= logy;

	return gf2_table_16.exp[q];
}

void galois_init_table(int w)
{
	if(w == GF2_INDEX_8)
	{
		if(!gf2_flag_8)
		{
			galois_field_create_tables(GF2_INDEX_8, &gf2_table_8);
			gf2_flag_8 = 1;
		}
	}
	else if(w == GF2_INDEX_16)
	{
		if(!gf2_flag_16)
		{
			galois_field_create_tables(GF2_INDEX_16, &gf2_table_16);
			gf2_flag_16 = 1;
		}
	}
}

void galois_free_table(void)
{
	if(gf2_flag_8)
	{
		free(gf2_table_8.log);
		free(gf2_table_8.exp);
		gf2_table_8.log = NULL;
		gf2_table_8.exp = NULL;
		if(gf2_table_8.mult)
		{
			free(gf2_table_8.mult);
			gf2_table_8.mult = NULL;
			free(gf2_table_8.div);
			gf2_table_8.div = NULL;
		}
		gf2_flag_8 = 0;
	}

	if(gf2_flag_16)
	{
		free(gf2_table_16.log);
		free(gf2_table_16.exp);
		gf2_table_16.log = NULL;
		gf2_table_16.exp = NULL;
		gf2_flag_16 = 0;
	}
}
