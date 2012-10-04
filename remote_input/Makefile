common = log.o communicator.o server.o server_test.o
CFLAGS = -Wall -O2
CC = gcc
#CC = i586-mingw32msvc-gcc

linux: $(common)
	$(CC) -o server_test $(common) -lpthread

win32: $(common)
	$(CC) -o server_test.exe $(common) -lpthread -lwsock32

.PHONY: clean
clean:
	rm -f server_test server_test.exe $(common)

