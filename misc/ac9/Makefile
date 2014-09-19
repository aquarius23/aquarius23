object = jpeg.o
CFLAGS = -Wall -O2
CC = gcc

mysdl: $(object)
	$(CC) -o jpeg $(object) -ljpeg -lexif

jpeg.o: jpeg.c

.PHONY: clean
clean:
	rm -f jpeg $(object)

