.PHONY: all

all: ./src/scgreengrab/screen.so ./src/readmem/readmem.so

./src/scgreengrab/screen.so: ./src/screengrab/screen.c
	gcc -march=native -shared -O3 -ffast-math -lX11 -fPIC -Wl,-soname,screen -o ./src/screengrab/screen.so ./src/screengrab/screen.c

./src/readmem/readmem.so: ./src/readmem/readmem.c
	gcc -march=native -shared -O3 -ffast-math -lX11 -fPIC -Wl,-soname,screen -o ./src/readmem/readmem.so ./src/readmem/readmem.c

./output/screen: ./src/screengrab/screen.c
	gcc -Wall -ggdb -lX11 -fPIC -o ./output/screen ./src/screengrab/screen.c
