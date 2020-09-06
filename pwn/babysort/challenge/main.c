#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef int (*SORTFUNC)(const void*, const void*);

typedef struct {
  long elm[5];
  SORTFUNC cmp[2];
} SortExperiment;

/* call me! */
void win(void) {
  char *args[] = {"/bin/sh", NULL};
  execve(args[0], args, NULL);
}

int cmp_asc(const void *a, const void *b) { return *(long*)a - *(long*)b; }
int cmp_dsc(const void *a, const void *b) { return *(long*)b - *(long*)a; }

int main(void) {
  SortExperiment se = {.cmp = {cmp_asc, cmp_dsc}};
  int i;

  /* input numbers */
  puts("-*-*- Sort Experiment -*-*-");
  for(i = 0; i < 5; i++) {
    printf("elm[%d] = ", i);
    if (scanf("%ld", &se.elm[i]) != 1) exit(1);
  }

  /* sort */
  printf("[0] Ascending / [1] Descending: ");
  if (scanf("%d", &i) != 1) exit(1);
  qsort(se.elm, 5, sizeof(long), se.cmp[i]);

  /* output result */
  puts("Result:");
  for(i = 0; i < 5; i++) {
    printf("elm[%d] = %ld\n", i, se.elm[i]);
  }
  return 0;
}

__attribute__((constructor))
void setup(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(300);
}
