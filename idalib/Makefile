object = gf2.o matrix.o ida.o test.o
CFLAGS = -Wall -O2
CC = gcc

idalib: $(object)
	$(CC) -o idatest $(object)

gf2.o: gf2.h gf2.c
matrix.o: matrix.h matrix.c
ida.o: ida.h ida.c
test.o: ida.h test.c

.PHONY: clean
clean:
	rm -f idatest $(object)

