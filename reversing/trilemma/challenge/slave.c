#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <link.h>
#include <sys/mman.h>

#define ADDR_SLAVE_SECRET (void*)0x3f5500000000
#define ADDR_SLAVE_FLAG   (void*)0x3fcc00000000

unsigned char slave_enc[] = {0x3c, 0x29, 0x11, 0xec, 0x8a, 0xf4, 0x69, 0x3d, 0x9a, 0xf2, 0x51, 0xd4, 0xfa, 0xdd, 0x44, 0xe7, 0xc4, 0xbf, 0xba};

unsigned char *emperor_secret(void);

unsigned char *slave_secret(void) {
  int i, j;
  unsigned char *secret;
  secret = mmap(ADDR_SLAVE_SECRET, 0x1000, PROT_READ | PROT_WRITE,
                MAP_POPULATE | MAP_PRIVATE | MAP_ANONYMOUS,
                -1, 0);
  if (secret != ADDR_SLAVE_SECRET) {
    fputs("[libslave.so] Resource conflicts.\n", stderr);
    exit(1);
  }

  for(i = 0; i < 0x100; i++) secret[i] = i;
  for(i = 0, j = 0; i < 0x55; i++) {
    j = (j + secret[i] + (((unsigned long)secret >> (i%8)*8) & 0xff)) % 0x100;
    unsigned char tmp;
    tmp = secret[i];
    secret[i] = secret[j];
    secret[j] = tmp;
  }

  return secret;
}

char *slave_flag(void) {
  unsigned char i, j;
  int n;
  unsigned char *flag;
  flag = mmap(ADDR_SLAVE_FLAG, 0x1000, PROT_READ | PROT_WRITE,
              MAP_POPULATE | MAP_PRIVATE | MAP_ANONYMOUS,
              -1, 0);
  if (flag != ADDR_SLAVE_FLAG) {
    fputs("[libslave.so] Resource conflicts.\n", stderr);
    exit(1);
  }

  unsigned char *S = emperor_secret();
  for(i = 0, j = 0, n = 0; n < 0x13; n++) {
    unsigned char tmp;
    i++;
    j = j + S[i];
    tmp = S[i];
    S[i] = S[j];
    S[j] = tmp;
    flag[n] = slave_enc[n] ^ S[(S[i] + S[j]) % 0x100];
  }

  return flag;
}

static int lookup(struct dl_phdr_info *info, size_t size, void *data) {
  int *result = (int*)data;
  if (strstr(info->dlpi_name, "libcitizen.so")) result[0] = 1;
  if (strstr(info->dlpi_name, "libemperor.so")) result[1] = 1;
  return 0;
}

__attribute__((constructor))
void slave(void) {
  int result[2] = {0};
  dl_iterate_phdr(lookup, (void*)result);
  if (result[0]) {
    fputs("[libslave.so] Citizen despises slave.\n", stderr);
    exit(1);
  }
  if (!result[1]) {
    fputs("[libslave.so] Slave thirsts for rebellion.\n", stderr);
    exit(1);
  }
}
