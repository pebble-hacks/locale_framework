#pragma once
#include "hash.h"

#ifndef STRINGIFY
  #define STRINGIFY_NX(a) #a
  #define STRINGIFY(a) STRINGIFY_NX(a)
#endif // STRINGIFY

#define DO_PRAGMA(x) _Pragma(#x)

#define DUMP_LOG_STRINGS_NX(label, s) DO_PRAGMA(message label s)

#define DUMP_LOG_STRINGS(label, s) \
    DUMP_LOG_STRINGS_NX(label, __FILE_NAME__ ":" s)

//extern DictionaryIterator s_locale_dict;

//static __attribute__((always_inline)) inline char *get_str(int hashval) { 
//  return dict_find(&s_locale_dict, hashval)->value->cstring; 
//}

#define LOC(str) get_str(HASH_DJB2(str))

void locale_init(void);
char *get_str(int hashval);


