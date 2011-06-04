#ifndef GF2_H
#define GF2_H

#define GF2_INDEX_8		8
#define GF2_INDEX_16	16

struct gf2_table 
{
	int		index;
	unsigned short	*log;
	unsigned short	*exp;
	unsigned char	*mult;
	unsigned char	*div;
};

unsigned char galois_multiply_w8(unsigned char x, unsigned char y);
unsigned char galois_divide_w8(unsigned char x, unsigned char y);
unsigned short galois_multiply_w16(unsigned short x, unsigned short y);
unsigned short galois_divide_w16(unsigned short x, unsigned short y);
void galois_init_table(int w);
void galois_free_table(void);

#endif
