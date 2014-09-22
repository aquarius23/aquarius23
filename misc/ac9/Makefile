object = jpeg.o main.o
CFLAGS = -Wall -O2
CC = gcc

main: $(object)
	$(CC) -o jpeg $(object) -ljpeg -lexif

jpeg.o: jpeg.c
main.o: main.c
.PHONY: clean
clean:
	rm -f jpeg $(object)

