/*
 * Do you know how WebKit keeps variables in memory?
 *
 * > The top 16-bits denote the type of the encoded JSValue:
 * >
 * >     Pointer {  0000:PPPP:PPPP:PPPP
 * >              / 0001:****:****:****
 * >     Double  {         ...
 * >              \ FFFE:****:****:****
 * >     Integer {  FFFF:0000:IIII:IIII
 *
 * How smart it is! I implemented this structure in C :)
 * I hope I made it right......
 *
 * Read the following code for more information:
 *  - https://github.com/adobe/webkit/blob/master/Source/JavaScriptCore/runtime/JSValue.h
 */

#define VALUE_UNDEFINED ((void*)0x0a)
#define MAGIC_STRING  0x0000
#define MAGIC_INTEGER 0xFFFF

/* A magic type that can keep string, double and integer! */
typedef union __attribute__((packed)) {
  char *String;
  double Double;
  int Integer;
  struct __attribute__((packed)) {
    unsigned long  data : 48;
    unsigned short magic: 16;
  } data;
} Value;

void Value_SetUndefined(Value *v) {
  v->String = VALUE_UNDEFINED;
}
void Value_SetString(Value *v, char *p) {
  v->String = p;
}
void Value_SetDouble(Value *v, double d) {
  v->Double = d;
}
void Value_SetInteger(Value *v, int i) {
  v->Integer = i;
  v->data.magic = MAGIC_INTEGER;
}

int Value_IsUndefined(Value v) {
  return v.String == VALUE_UNDEFINED;
}
int Value_IsString(Value v) {
  return (v.data.magic == MAGIC_STRING) && (!Value_IsUndefined(v));
}
int Value_IsInteger(Value v) {
  return v.data.magic == MAGIC_INTEGER;
}
int Value_IsDouble(Value v) {
  return !(Value_IsUndefined(v) || Value_IsString(v) || Value_IsInteger(v));
}
