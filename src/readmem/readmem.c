#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/wait.h>

#define MAGIC_PATTERN 0x3c8f3c8f3c8f3c8f
#define MAGIC_OFFSET  0x0440
#define DEBUG 0
#define debug(fmt, ...) do { if (DEBUG) fprintf(stderr, fmt, __VA_ARGS__); } while (0)

int get_player_rank(const int pid, const long address) {
  debug("get_player_rank: start_address 0x%lx\n", address);

  int ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);
  wait(NULL);
  debug("get_player_rank: ptrace attach return %d\n", ret);

  long byte = ptrace(PTRACE_PEEKTEXT, pid, address, 4);
  long player_rank = (byte + 2) / 2;

  debug("get_player_rank: rank is %ld found at 0x%lx\n", player_rank, address);

  ptrace(PTRACE_DETACH, pid, NULL, NULL);
  return player_rank;
}

long find_player_rank_address(const int pid, const long heap_start) {
  debug("find_magic_location: using pid %d with heap at 0x%lx\n", pid, heap_start);

  int ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);
  wait(NULL);
  debug("find_player_rank_address: ptrace attach return %d\n", ret);

  long loc;

  for(long i = 0; i < 0xffffff; i += 16) {
    long byte;
    loc = heap_start + i;
    byte = ptrace(PTRACE_PEEKTEXT, pid, loc, 16);
    if (byte == MAGIC_PATTERN) {
      debug("find_magic_location: found magic 0x%lx at 0x%lx\n", byte, loc);
      break;
    }
  }

  ptrace(PTRACE_DETACH, pid, NULL, NULL);
  return loc + MAGIC_OFFSET;
}
