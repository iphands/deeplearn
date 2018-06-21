.PHONY: all clean
.DEFAULT_GOAL := all

CFLAGS=-march=native -O3 -ffast-math

clean:
	rm -f \
	./src/screengrab/screen.so \
	./src/readmem/readmem.so \
	./src/utils/monitor.bin

all: ./src/screengrab/screen.so ./src/readmem/readmem.so ./src/utils/monitor.bin

./src/utils/monitor.bin: ./src/utils/monitor.c
	gcc ${CFLAGS} -lX11 -o ./src/utils/monitor.bin ./src/utils/monitor.c

./src/screengrab/screen.so: ./src/screengrab/screen.c
	gcc ${CFLAGS} -shared -lX11 -fPIC -Wl,-soname,screen -o ./src/screengrab/screen.so ./src/screengrab/screen.c

./src/readmem/readmem.so: ./src/readmem/readmem.c
	gcc ${CFLAGS} -shared -lX11 -fPIC -Wl,-soname,screen -o ./src/readmem/readmem.so ./src/readmem/readmem.c
