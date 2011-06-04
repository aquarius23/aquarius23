#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "gf2.h"
#include "matrix.h"
#include "ida.h"

char *str = "123456789abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz";
char split[256];
char key[256];
char combine[256];

void test1(void)
{
	char *p;
	int size;
	struct ida_data *ida;
	ida = create_ida(1, 11, 8);
	encode_data(ida, str);
	{
		p = get_key_vector(ida, 0, &size);
		memcpy(key + size * 0, p, size);
		p = get_split_vector(ida, 0, &size);
		memcpy(split + size * 0, p, size);

		p = get_key_vector(ida, 2, &size);
		memcpy(key + size * 1, p, size);
		p = get_split_vector(ida, 2, &size);
		memcpy(split + size * 1, p, size);

		p = get_key_vector(ida, 3, &size);
		memcpy(key + size * 2, p, size);
		p = get_split_vector(ida, 3, &size);
		memcpy(split + size * 2, p, size);

		p = get_key_vector(ida, 5, &size);
		memcpy(key + size * 3, p, size);
		p = get_split_vector(ida, 5, &size);
		memcpy(split + size * 3, p, size);

		p = get_key_vector(ida, 6, &size);
		memcpy(key + size * 4, p, size);
		p = get_split_vector(ida, 6, &size);
		memcpy(split + size * 4, p, size);

		p = get_key_vector(ida, 7, &size);
		memcpy(key + size * 5, p, size);
		p = get_split_vector(ida, 7, &size);
		memcpy(split + size * 5, p, size);

		p = get_key_vector(ida, 8, &size);
		memcpy(key + size * 6, p, size);
		p = get_split_vector(ida, 8, &size);
		memcpy(split + size * 6, p, size);

		p = get_key_vector(ida, 9, &size);
		memcpy(key + size * 7, p, size);
		p = get_split_vector(ida, 9, &size);
		memcpy(split + size * 7, p, size);
	}
//	set_combine_matrix(ida, key);
//	decode_data(ida, split, combine);
	{
		struct gf2_matrix *matrix = set_another_combine_matrix(ida,key);
		another_decode_data(ida, matrix, split, combine);
		free_another_matrix(matrix);
	}
	free_ida(ida);
}

void test2(void)
{
	int i, size, count;
	char *p;
	struct ida_data *ida;
	ida = create_ida(1, 8, 8);
	encode_data(ida, str);
	for(i = 0; i < 8; i++)
	{
		p = get_key_vector(ida, i, &size);
		memcpy(key + size * i, p, size);
		p = get_split_vector(ida, i, &size);
		memcpy(split + size * i, p, size);
	}

	count = 320000;
	while(count--)
	{
		encode_data(ida, str);
	}

	set_combine_matrix(ida, key);
	decode_data(ida, split, combine);
	free_ida(ida);
}

void stub(void)
{
	test1();
	test2();
}
