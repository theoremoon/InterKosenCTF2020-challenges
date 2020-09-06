#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define anti_ida_decompiler                     \
  __asm__ ("  push     r8       \n"             \
           "  push     rsi      \n"             \
           "  push     rcx      \n"             \
           "  push     rax      \n"             \
           "  xor      eax, eax \n"             \
           "  jz       opaque   \n"             \
           "  add      rsp, 777 \n"             \
           "opaque:             \n"             \
           "  pop      rax      \n"             \
           "  pop      rcx      \n"             \
           "  pop      rsi      \n"             \
           "  pop      r8       \n");

char answer[] = {219, 226, 235, 247, 214, 237, 235, 197, 232, 162, 171, 238, 216, 193, 174, 183, 196, 197, 241, 176, 171, 193, 208, 190, 231, 186, 214, 206, 235, 159};

int check(unsigned char *flag, unsigned char *ans) {
  int i, l = strlen(flag);
  anti_ida_decompiler;
  for(i = 0; i < l; i++) {
    if ((flag[i] ^ flag[i+1] ^ i ^ 0xff) != ans[i]) {
      return 1;
    }
  }
  return 0;
}

int main(int argc, char **argv) {
  if (argc < 2) {
    printf("Usage: %s <FLAG>\n", argv[0]);
    return 1;
  }

  if (check(argv[1], answer) == 0) {
    puts("Correct!");
  } else {
    puts("Wrong...");
  }
  return 0;
}
