#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

struct __attribute__((packed)) {
  char buf[0x200];
  FILE *fp;
} core;

void win(void) {
  char *args[] = {"/bin/sh", NULL};
  write(1, "Congratulations!\n", 0x11);
  execve(args[0], args, NULL);
}

void vuln(void) {
  printf("<win> = %p\n", &win);
  gets(core.buf);
  puts(core.buf);
}

int main(void) {
  core.fp = fopen("banner.txt", "r");
  if (core.fp == NULL) {
    perror("banner.txt");
    return 1;
  } else {
    fread(core.buf, 1, sizeof(core.buf), core.fp);
    puts(core.buf);
    vuln();
    fclose(core.fp);
    return 0;
  }
}

__attribute__((constructor))
void setup(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(60);
}
