#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "type.h"
#define NUM_ELEMENT 10

Value list[NUM_ELEMENT];

/* Utils */
char *get_string(const char *msg) {
  char *ptr, *nlpos;
  size_t n = 0;
  printf("%s", msg);
  if (getline(&ptr, &n, stdin) == -1) {
    free(ptr);
    exit(0);
  }
  if (nlpos = strchr(ptr, '\n')) {
    *nlpos = '\0';
  }
  return ptr;
}
int get_integer(const char *msg) {
  char *p = get_string(msg);
  int v = atoi(p);
  free(p);
  return v;
}
double get_double(const char *msg) {
  char *p = get_string(msg);
  double v = atof(p);
  free(p);
  return v;
}
int menu(void) {
  puts("1. Set value");
  puts("2. Show list");
  puts("3. Delete value");
  return get_integer("> ");
}

/* List operation */
void set(void) {
  unsigned int index, type;

  index = get_integer("index: ");
  if (index >= NUM_ELEMENT) {
    puts("Wrong index :(");
    return;
  }

  if (Value_IsString(list[index]))
    free(list[index].String);

  type = get_integer("type (1=String / 2=Double / 3=Integer): ");
  switch(type) {
  case 1:
    Value_SetString(&list[index], get_string("data: "));
    break;
  case 2:
    Value_SetDouble(&list[index], get_double("data: "));
    break;
  case 3:
    Value_SetInteger(&list[index], get_integer("data: "));
    break;
  default:
    Value_SetUndefined(&list[index]);
    puts("Wrong type :(");
    return;
  }

  puts("[+] Successfully set value");
}

void print(void) {
  int i;
  puts("list {");
  for (i = 0; i < NUM_ELEMENT; i++) {
    if (Value_IsUndefined(list[i])) {
      printf("  %d: undefined\n", i);
    } else if (Value_IsString(list[i])) {
      printf("  %d: [string] \"%s\"\n", i, list[i].String);
    } else if (Value_IsInteger(list[i])) {
      printf("  %d: [integer] %d\n", i, list[i].Integer);
    } else if (Value_IsDouble(list[i])) {
      printf("  %d: [double] %f\n", i, list[i].Double);
    }
  }
  puts("}");
}

void delete(void) {
  unsigned int index, type;

  index = get_integer("index: ");
  if (index >= NUM_ELEMENT) {
    puts("Wrong index :(");
    return;
  }

  if (Value_IsString(list[index]))
    free(list[index].String);

  Value_SetUndefined(&list[index]);
  puts("[+] Successfully deleted value");
}

/* Entry Point */
int main(void) {
  int i;
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  for(i = 0; i < NUM_ELEMENT; i++)
    Value_SetUndefined(&list[i]);

  while(1) {
    switch(menu()) {
    case 1: set(); break;
    case 2: print(); break;
    case 3: delete(); break;
    default: return 0;
    }
  }
}
