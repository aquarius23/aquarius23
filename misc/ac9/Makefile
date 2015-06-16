object1 = jpeg.o main.o merge.o utils.o
object2 = jpeg.o main2.o yuv2rgb.o
CFLAGS = -Wall -O2
CC = g++

main: $(object1) $(object2)
	$(CC) -o jpeg $(object1) -ljpeg -lexif -lshla -L.
	$(CC) -o yuv2jpeg $(object2) -ljpeg -lexif -L.

jpeg.o: jpeg.c
merge.o: merge.c
utils.o: utils.c
main.o: main.c
main2.o: main2.c
yuv2rgb.o: yuv2rgb.c
.PHONY: clean
clean:
	rm -f jpeg yuv2jpeg $(object1) $(object2)


