#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <unistd.h>

int w = 300;
int h = 300;

int main () {
  Display *dpy = XOpenDisplay(":0.0");
  Window root = XCreateSimpleWindow(dpy, DefaultRootWindow(dpy), 10, 10, w, h, 1, 0, 0);

  GC gc = XCreateGC(dpy, root, 0, 0);
  XMapWindow(dpy, root);

  Display * snoop_dpy  = XOpenDisplay(NULL);
  Window    snoop_root = RootWindow(snoop_dpy, 0);
  XWindowAttributes win_info;

  while (1) {
    XGetWindowAttributes(snoop_dpy, snoop_root, &win_info);
    XImage * img = XGetImage(snoop_dpy, snoop_root, 0, 0, w, h, AllPlanes, ZPixmap);
    XPutImage(dpy, root, gc, img, 0, 0, 0, 0, img->width, img->height );
    XDestroyImage(img);
    usleep(1000 * 2);
  }

  XCloseDisplay (dpy);
}
