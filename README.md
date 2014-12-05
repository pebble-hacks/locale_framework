# locale_framework

Minimal framework to support locale features in Pebble apps, using 
[`i18n_get_system_locale()`](http://developer.getpebble.com/docs/c/group___internationalization.html) 
in Pebble Firmware 2.8+ to discover the system locale and select the correct
text to display.

## To Use

* Add `localize.h`, `localize.c` and `hash.h` to your project's `src` directory.  

* Add `locale_english.bin`, `locale_french.bin`, `locale_spanish.bin` and
  `locale_german.bin` to your app resources.

> Note: Empty files (size 0) are used as placeholders so code can compile, and
> will fall back to English.

* Add `#include <localize.h>` to any code files using the framework.

* Modify your main function to use `init_locale()`:

```c
int main(void) {
  locale_init();

  /* ... */

}
```

* All strings that you wish to localize, add `_()` around them.

```c
_("Press the select button");
```

* Run `python gen_dict.py src/ locale_english.json`. This will generate
  `locale_english.json` and `locale_english.bin`.

* Copy `locale_english.bin` to your project's `resources` directory.

* Copy `locale_english.json` to other languages, such as `locale_german.json`.

* Modify `locale_german.json` to replace the English strings with German
  strings.

* Run `python dict2bin.py locale_german.json`. This will generate
  `locale_german.bin`.

* Copy `locale_german.bin` to your project's `resources` directory.

* Add the following to your appinfo.json to declare the raw resource files:

```js
"media": [
  {
    "type": "raw",
    "name": "LOCALE_ENGLISH",
    "file": "locale_english.bin"
  }, 
  {
    "type": "raw",
    "name": "LOCALE_FRENCH",
    "file": "locale_french.bin"
  }, 
  {
    "type": "raw",
    "name": "LOCALE_SPANISH",
    "file": "locale_spanish.bin"
  }, 
  {
    "type": "raw",
    "name": "LOCALE_GERMAN",
    "file": "locale_german.bin"
  }
]
```

* Compile application and install!

> Note: `localize.c` is hard-coded to simplify testing (currently Spanish),
> modify `localize.c` lines 7 & 8 to use automatically detected system locale.
