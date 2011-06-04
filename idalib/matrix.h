#ifndef MATRIX_H
#define MATRIX_H

struct gf2_matrix
{
	int rows;
	int cols;
	int width;
	unsigned char *values;
};

struct key_list
{
	int width;
	int *values;
};

struct gf2_matrix *alloc_empty_matrix(int w, int n, int m);
struct gf2_matrix *generate_cauchy_matrix(int w, int n, int m);
void free_matrix(struct gf2_matrix *matrix);
struct gf2_matrix *revert_matrix(struct gf2_matrix * matrix);
int multiply_matrix(struct gf2_matrix *a, struct gf2_matrix *b, struct gf2_matrix *c);

#endif
