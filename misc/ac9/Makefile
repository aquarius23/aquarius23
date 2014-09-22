object = jpeg.o main.o merge.o utils.o
CFLAGS = -Wall -O2
CC = g++

main: $(object)
	$(CC) -o jpeg $(object) -ljpeg -lexif -lshla -L.

jpeg.o: jpeg.c
merge.o: merge.c
utils.o: utils.c
main.o: main.c
.PHONY: clean
clean:
	rm -f jpeg $(object)

