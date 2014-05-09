object = sdl.o
CFLAGS = -Wall -O2
CC = gcc

mysdl: $(object)
	$(CC) -o mysdl $(object) -lSDL

sdl.o: sdl.c

.PHONY: clean
clean:
	rm -f mysdl $(object)

