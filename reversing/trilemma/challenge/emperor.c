#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <link.h>
#include <sys/mman.h>

#define ADDR_EMPEROR_SECRET (void*)0x3fee00000000
#define ADDR_EMPEROR_FLAG   (void*)0x3f5500000000

unsigned char emperor_enc[] = {0x37, 0x49, 0x8d, 0xe4, 0x38, 0x8e, 0x2c, 0xce, 0x91, 0x21, 0x40, 0xb5, 0xed, 0xe5, 0xa6, 0x91, 0x93, 0x7a, 0xc8};

unsigned char *citizen_secret(void);

unsigned char *emperor_secret(void) {
  int i, j;
  unsigned char *secret;
  secret = mmap(ADDR_EMPEROR_SECRET, 0x1000, PROT_READ | PROT_WRITE,
                MAP_POPULATE | MAP_SHARED | MAP_ANONYMOUS,
                -1, 0);
  if (secret != ADDR_EMPEROR_SECRET) {
    fputs("[libemperor.so] Resource conflicts.\n", stderr);
    exit(1);
  }

  for(i = 0; i < 0x100; i++) secret[i] = i;
  for(i = 0, j = 0; i < 0xee; i++) {
    j = (j + secret[i] + (((unsigned long)secret >> (i%8)*8) & 0xff)) % 0x100;
    unsigned char tmp;
    tmp = secret[i];
    secret[i] = secret[j];
    secret[j] = tmp;
  }

  return secret;
}

unsigned char *emperor_flag(void) {
  unsigned char i, j;
  int n;
  unsigned char *flag;
  flag = mmap(ADDR_EMPEROR_FLAG, 0x1000, PROT_READ | PROT_WRITE,
              MAP_POPULATE | MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED,
              -1, 0);
  if (flag != ADDR_EMPEROR_FLAG) {
    fputs("[libemperor.so] Resource conflicts.\n", stderr);
    exit(1);
  }

  unsigned char *S = citizen_secret();
  for(i = 0, j = 0, n = 0; n < 0x13; n++) {
    unsigned char tmp;
    i++;
    j = j + S[i];
    tmp = S[i];
    S[i] = S[j];
    S[j] = tmp;
    flag[n] = emperor_enc[n] ^ S[(S[i] + S[j]) & 0xff];
  }

  return flag;
}

static int lookup(struct dl_phdr_info *info, size_t size, void *data) {
  int *result = (int*)data;
  if (strstr(info->dlpi_name, "libslave.so")) result[0] = 1;
  if (strstr(info->dlpi_name, "libcitizen.so")) result[1] = 1;
  return 0;
}

__attribute__((constructor))
void emperor(void) {
  int result[2] = {0};
  dl_iterate_phdr(lookup, (void*)result);
  if (result[0]) {
    fputs("[libemperor.so] Slave makes revolution.\n", stderr);
    exit(1);
  }
  if (!result[1]) {
    fputs("[libemperor.so] Emperor leads citizen.\n", stderr);
    exit(1);
  }
}
