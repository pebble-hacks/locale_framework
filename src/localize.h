#pragma once
#include "hash.h"

#define LOC(str) get_locale_str(HASH_DJB2(str))

void locale_init(void);

char *get_locale_str(int hashval);

