object = jpeg.o main.o merge.o
CFLAGS = -Wall -O2
CC = gcc

main: $(object)
	$(CC) -o jpeg $(object) -ljpeg -lexif

jpeg.o: jpeg.c
merge.o: merge.c
main.o: main.c
.PHONY: clean
clean:
	rm -f jpeg $(object)

