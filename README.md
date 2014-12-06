# locale_framework

Minimal framework to support locale features in Pebble apps, using 
[`i18n_get_system_locale()`](http://developer.getpebble.com/docs/c/group___internationalization.html) 
in Pebble Firmware 2.8+ to discover the system locale and select the correct
text to display.

## To Use

### Setting Up Your Project

* Add `localize.h`, `localize.c` and `hash.h` to your project's `src` directory.  

* Add `locale_english.bin`, `locale_french.bin`, `locale_spanish.bin` and
  `locale_german.bin` to your app resources.

> Note: Empty files (size 0) are used as placeholders so code can compile, and
> will fall back to English.

* Add `#include <localize.h>` to any code files that require translation.

* Modify your main function to use `init_locale()`:

```c
int main(void) {
  // Init locale framework
  locale_init();

  /* Other app setup code */

}
```

* For all strings that you wish to localize, add `_()` around them.

```c
_("Breakfast Time");
```

### Generating Translation Resources

* Run `python gen_dict.py src/ locale_english.json`. This will generate
  `locale_english.json` and `locale_english.bin`.

* Move `locale_english.bin` to your project's `resources` directory.

* Make a copy of `locale_english.json` for other languages, such as
  `locale_german.json`.

* Modify `locale_german.json` to replace the English strings with German
  strings.

* Run `python dict2bin.py locale_german.json`. This will generate
  `locale_german.bin`.

* Move `locale_german.bin` to your project's `resources` directory.

* Add the new `.bin` resource files to your project's `appinfo.json` file as 
  shown in the 
  [App Resources guide](https://developer.getpebble.com/guides/pebble-apps/display-and-animations/resources/#raw-resources). 
  For example, for the four language files in this project are added as shown
  below:

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

* Compile your application and install!

You can easily test your translations by commenting line 11 and uncommenting
line 8 of `localize.c`, replacing "es" with a locale you are translating.

### Adding More Languages

If you wish to add more translations in the future, repeat *Generating
Translation Resources* to obtain new translation binary resources. You will also
need to do this in the event that you modify any of your strings.