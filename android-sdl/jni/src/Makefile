common = common.o testdraw2.o
CFLAGS = -Wall -O2
LINK_LIB = -lSDL2

ifeq ($(ARCH), win32)
CC = i586-mingw32msvc-gcc
extra_inc = ./win32_lib/include/SDL2/
extra_lib = ./win32_lib/lib/
POSTFIX = .exe
else
CC = gcc
extra_inc += ../SDL/include/
extra_lib = ./linux_lib/
endif
CFLAGS += -I$(extra_inc) -L$(extra_lib)

all: $(common)
	$(CC) -o mysdl$(POSTFIX) $(CFLAGS) $(common) $(LINK_LIB)

.PHONY: clean
clean:
	rm -f mysdl* *.o

