#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "gf2.h"
#include "matrix.h"
#include "ida.h"

char *str = "123456789abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz";
char encode[256];
char decode[256];
char key[256];


void test1(void)
{
	char *p;
	int index, size;
	struct ida_encode *enc;
	struct ida_decode *dec;
	enc = ida_encode_create(1, 11, 7);
	printf("block size = %d\n", ida_encode_block_size(enc));
	size = ida_encode_data(enc, str);
	printf("encode size = %d\n", size);
	
	//encode
	{
		index = 0;
		p = ida_encode_key_vector(enc, index, &size);
		memcpy(key + size * 0, p, size);
		p = ida_encode_output_vector(enc, index, &size);
		memcpy(encode + size * 0, p, size);

		index = 1;
		p = ida_encode_key_vector(enc, index, &size);
		memcpy(key + size * 1, p, size);
		p = ida_encode_output_vector(enc, index, &size);
		memcpy(encode + size * 1, p, size);

		index = 2;
		p = ida_encode_key_vector(enc, index, &size);
		memcpy(key + size * 2, p, size);
		p = ida_encode_output_vector(enc, index, &size);
		memcpy(encode + size * 2, p, size);

		index = 3;
		p = ida_encode_key_vector(enc, index, &size);
		memcpy(key + size * 3, p, size);
		p = ida_encode_output_vector(enc, index, &size);
		memcpy(encode + size * 3, p, size);

		index = 4;
		p = ida_encode_key_vector(enc, index, &size);
		memcpy(key + size * 4, p, size);
		p = ida_encode_output_vector(enc, index, &size);
		memcpy(encode + size * 4, p, size);

		index = 9;
		p = ida_encode_key_vector(enc, index, &size);
		memcpy(key + size * 5, p, size);
		p = ida_encode_output_vector(enc, index, &size);
		memcpy(encode + size * 5, p, size);

		index = 6;
		p = ida_encode_key_vector(enc, index, &size);
		memcpy(key + size * 6, p, size);
		p = ida_encode_output_vector(enc, index, &size);
		memcpy(encode + size * 6, p, size);

	}
	ida_encode_free(enc);

	//decode
	dec = ida_decode_create(1, 7);
	{
		int ret;
		ret = ida_decode_set_key(dec, key);
		if(ret > 0)
			ret = ida_decode_data(dec, encode, decode);
		printf("decode str : %s\n", decode);
		printf("ret size = %d\n", ret);
	}
	ida_decode_free(dec);
}

int main(void)
{
	test1();
	return 0;
}

