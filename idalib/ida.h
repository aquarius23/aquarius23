#ifndef IDA_H
#define IDA_H

struct ida_data
{
	int width;
	int n;
	int m;
	int size;
	struct gf2_matrix *key;
	struct gf2_matrix *reverse;
	struct gf2_matrix *split;
	struct gf2_matrix *encode;
	struct gf2_matrix *decode;
};

struct ida_data *create_ida(int width, int n, int m);
int get_ida_block_size(struct ida_data *ida);
void free_ida(struct ida_data *ida);
char *get_key_vector(struct ida_data *ida, int index, int *size);
char *get_split_vector(struct ida_data *ida, int index, int *size);
int set_combine_matrix(struct ida_data *ida, void *input);
void encode_data(struct ida_data *ida, void *input);
void decode_data(struct ida_data *ida, void *input, void *output);
struct gf2_matrix *set_another_combine_matrix(struct ida_data *ida, void *input);
void another_decode_data(struct ida_data *ida, struct gf2_matrix *matrix, void *input, void *output);
void free_another_matrix(struct gf2_matrix *matrix);

#endif
