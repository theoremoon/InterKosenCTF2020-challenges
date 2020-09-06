/**
   $ gcc main.c -L./ -lemperor -lcitizen -lslave
   $ LD_LIBRARY_PATH=./ ./a.out
 */
#include <stdio.h>

char *emperor_flag(void);
char *citizen_flag(void);
char *slave_flag(void);

int main(void) {
  printf("The flag is %s%s%s\n", emperor_flag(), citizen_flag(), slave_flag());
  return 0;
}
