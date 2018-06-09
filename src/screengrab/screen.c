#include <stdio.h>
#include <X11/X.h>
#include <X11/Xlib.h>

void getScreen(const int, const int, const int, const int, unsigned char *);
void init();

Display *display = NULL;
Window root = NULL;

int main(int argc, char* argv[]) {
  printf("SCREEN TEST\n");
}

void init() {
   display = XOpenDisplay(NULL);
   root = DefaultRootWindow(display);
}

void destroy() {
  XDestroyWindow(display, root);
  XCloseDisplay(display);
}

void get_image_rgb(const int window_origin_x,
               const int window_origin_y,
               const int window_width,
               const int window_height,
               unsigned char * data) {

  XImage *image = XGetImage(display,
                            root,
                            window_origin_x,
                            window_origin_y,
                            window_width,
                            window_height,
                            AllPlanes,
                            ZPixmap);

  unsigned long red_mask   = image->red_mask;
  unsigned long green_mask = image->green_mask;
  unsigned long blue_mask  = image->blue_mask;

  for (int y = 0, counter = 0; y < window_height; y++) {
    for (int x = 0; x < window_width; x++) {
      unsigned long pixel = XGetPixel(image, x, y);
      unsigned char blue  = (pixel & blue_mask);
      unsigned char green = (pixel & green_mask) >> 8;
      unsigned char red   = (pixel & red_mask)   >> 16;

      data[counter + 2] = blue;
      data[counter + 1] = green;
      data[counter + 0] = red;
      counter += 3;
    }
  }

  XDestroyImage(image);
}

void get_image_grey(const int window_origin_x,
               const int window_origin_y,
               const int window_width,
               const int window_height,
               unsigned char * data) {

  XImage *image = XGetImage(display,
                            root,
                            window_origin_x,
                            window_origin_y,
                            window_width,
                            window_height,
                            AllPlanes,
                            ZPixmap);

  unsigned int counter = 0;

  /* #pragma omp parallel for collapse(2) */
  for (int y = 0; y < window_height; y++) {
    for (int x = 0; x < window_width; x++) {
      unsigned long pixel = XGetPixel(image, x, y);
      unsigned char blue  = (pixel & image->blue_mask);
      unsigned char green = (pixel & image->green_mask) >> 8;
      unsigned char red   = (pixel & image->red_mask)   >> 16;
      unsigned char val   = (red + blue + green) / 3;
      data[counter] = val;
      counter += 1;
    }
  }


  XDestroyImage(image);
}
