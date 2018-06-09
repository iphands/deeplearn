./src/scgreengrab/screen.so: ./src/screengrab/screen.c
	gcc -march=native -shared -O3 -ffast-math -lX11 -fPIC -Wl,-soname,screen -o ./src/screengrab/screen.so ./src/screengrab/screen.c

./output/screen: ./src/screengrab/screen.c
	gcc -Wall -ggdb -lX11 -fPIC -o ./output/screen ./src/screengrab/screen.c
