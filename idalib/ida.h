#ifndef IDA_H
#define IDA_H

struct ida_encode
{
	int width;
	int n;
	int m;
	int size;
	struct gf2_matrix *key;
	struct gf2_matrix *input;
	struct gf2_matrix *output;
};

struct ida_decode
{
	int width;
//	int n;
	int m;
	int size;
	struct gf2_matrix *key;
	struct gf2_matrix *input;
	struct gf2_matrix *output;
};

struct ida_encode *ida_encode_create(int width, int n, int m);
void ida_encode_free(struct ida_encode *ida);
int ida_encode_block_size(struct ida_encode *ida);
int ida_encode_data(struct ida_encode *ida, void *input);
char *ida_encode_key_vector(struct ida_encode *ida, int index, int *size);
char *ida_encode_output_vector(struct ida_encode *ida, int index, int *size);

struct ida_decode *ida_decode_create(int width, int m);
void ida_decode_free(struct ida_decode *ida);
int ida_decode_set_key(struct ida_decode *ida, void *input);
int ida_decode_data(struct ida_decode *ida, void *input, void *output);
#endif

