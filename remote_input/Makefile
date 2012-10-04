common = log.o communicator.o server.o client.o 
server = server_test.o
client = client_test.o

CFLAGS = -Wall -O2
CC = gcc
#CC = i586-mingw32msvc-gcc

linux: $(common) $(server) $(client)
	$(CC) -o server_test $(common) $(server) -lpthread
	$(CC) -o client_test $(common) $(client) -lpthread

win32: $(common) $(server) $(client)
	$(CC) -o server_test.exe $(common) $(server) -lpthread -lwsock32
	$(CC) -o client_test.exe $(common) $(client) -lpthread -lwsock32

.PHONY: clean
clean:
	rm -f server_test server_test.exe client_test client_test.exe $(common) $(server) $(client)

