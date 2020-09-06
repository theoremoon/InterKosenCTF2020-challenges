#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <link.h>
#include <sys/mman.h>

#define ADDR_CITIZEN_SECRET (void*)0x3fcc00000000
#define ADDR_CITIZEN_FLAG   (void*)0x3fee00000000

unsigned char citizen_enc[] = {0x3f, 0x75, 0x7f, 0x03, 0x07, 0x39, 0x51, 0x84, 0x07, 0x91, 0x7e, 0xd0, 0xa8, 0xd9, 0x09, 0xe6, 0x24, 0x43, 0x8f};

unsigned char *slave_secret(void);

unsigned char *citizen_secret(void) {
  int i, j;
  unsigned char *secret;
  secret = mmap(ADDR_CITIZEN_SECRET, 0x1000, PROT_READ | PROT_WRITE,
                MAP_POPULATE | MAP_PRIVATE | MAP_ANONYMOUS,
                -1, 0);
  if (secret != ADDR_CITIZEN_SECRET) {
    fputs("[libcitizen.so] Resource conflicts.\n", stderr);
    exit(1);
  }

  for(i = 0; i < 0x100; i++) secret[i] = i;
  for(i = 0, j = 0; i < 0xcc; i++) {
    j = (j + secret[i] + (((unsigned long)secret >> (i%8)*8) & 0xff)) % 0x100;
    unsigned char tmp;
    tmp = secret[i];
    secret[i] = secret[j];
    secret[j] = tmp;
  }

  return secret;
}

unsigned char *citizen_flag(void) {
  unsigned char i, j;
  int n;
  unsigned char *flag;
  flag = mmap(ADDR_CITIZEN_FLAG, 0x1000, PROT_READ | PROT_WRITE,
              MAP_POPULATE | MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED,
              -1, 0);
  if (flag != ADDR_CITIZEN_FLAG) {
    fputs("[libcitizen.so] Resource conflicts.\n", stderr);
    exit(1);
  }

  unsigned char *S = slave_secret();
  for(i = 0, j = 0, n = 0; n < 0x13; n++) {
    unsigned char tmp;
    i++;
    j = j + S[i];
    tmp = S[i];
    S[i] = S[j];
    S[j] = tmp;
    flag[n] = citizen_enc[n] ^ S[(S[i] + S[j]) & 0xff];
  }

  return flag;
}

static int lookup(struct dl_phdr_info *info, size_t size, void *data) {
  int *result = (int*)data;
  if (strstr(info->dlpi_name, "libemperor.so")) result[0] = 1;
  if (strstr(info->dlpi_name, "libslave.so")) result[1] = 1;
  return 0;
}

__attribute__((constructor))
void citizen(void) {
  int result[2] = {0};
  dl_iterate_phdr(lookup, (void*)result);
  if (result[0]) {
    fputs("[libcitizen.so] Emperor manipulates citizen.\n", stderr);
    exit(1);
  }
  if (!result[1]) {
    fputs("[libcitizen.so] Citizen needs labor.\n", stderr);
    exit(1);
  }
}
