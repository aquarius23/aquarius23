common = common.o testdraw2.o
CFLAGS = -Wall -O2 -I../SDL/include
LINK_LIB = -lSDL2

ifeq ($(ARCH), win32)
CC = i586-mingw32msvc-gcc
extra_lib = ./win32_lib/
POSTFIX = .exe
else
CC = gcc
extra_lib = ./linux_lib/
endif
CFLAGS += -L$(extra_lib)

all: $(common)
	$(CC) -o mysdl$(POSTFIX) $(CFLAGS) $(common) $(LINK_LIB)

.PHONY: clean
clean:
	rm -f mysdl* *.o

