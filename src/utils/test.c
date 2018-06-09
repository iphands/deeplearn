#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/wait.h>

int main (int argc, char *argv[]) {
  int pid = atoi(argv[1]);
  long heap_start = strtol(argv[2], NULL, 16);
  printf("Using pid %d with heap at 0x%lx\n", pid, heap_start);

  ptrace(PTRACE_ATTACH, pid, NULL, NULL);
  wait(NULL);

  long loc, byte, prev;

  for (long i = 0; i < 0xffffff; i += 16) {
    loc = heap_start + i;
    long offset = loc - heap_start;
    byte = ptrace(PTRACE_PEEKTEXT, pid, loc, 16);

    if (byte == 0x3c8f3c8f3c8f3c8f) {
      printf("debug: found magic %lx (0x%05x) %lx\n", loc, offset, byte);
      break;
    }

    prev = byte;
  }

  byte = ptrace(PTRACE_PEEKTEXT, pid, (loc + 0x0440), 4);
  byte = (byte + 2) / 2;
  printf("debug: cheat try     place is %d\n", byte);

  ptrace(PTRACE_DETACH, pid, NULL, NULL);
}
