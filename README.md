locale_framework
================
Minimal framework to support locale feature in Pebble apps.
locale_framework uses i18n_get_locale in Pebble Firmware 2.8+ to discover the system locale and select the correct text to display.

To use:
Add localize.h, localize.c and hash.h to your projects source code. 
Add locale_english.bin locale_french.bin locale_spanish.bin locale_german.bin to your resources  
  note: empty files (size 0) are used as placeholders so code can compile, and will fall back to English.
Add #include <localize.h> to your source code  
Modify your main function to init_locale():
{code}
int main(void) {
  locale_init();
{code}
All strings that you wish to localize, add LOC() around them  
  ex. LOC("Press the select button")  
Run `python gen_dict.py src/ locale_english.json`  
This will generate locale_english.json and locale_english.bin
Copy locale_english.bin to resources/
Copy locale_english.json to other languages, such as locale_german.json  
Modify locale_german.json to replace the English strings with German strings  
Run `python dict2bin.py locale_german.json`  
This will generate locale_german.bin  
Copy locale_german.bin to resources/

Add the following to your appinfo.json
{code}
 "media": [
    {
      "type": "raw",
      "name": "LOCALE_ENGLISH",
      "file": "locale_english.bin"
    }, {
      "type": "raw",
      "name": "LOCALE_FRENCH",
      "file": "locale_french.bin"
    }, {
      "type": "raw",
      "name": "LOCALE_SPANISH",
      "file": "locale_spanish.bin"
    }, {
      "type": "raw",
      "name": "LOCALE_GERMAN",
      "file": "locale_german.bin"
    }
    ]
  {code}
  
  Compile application and install  
  Note: localize.c is hard-coded to simplify testing (currently Spanish), modify localize.c lines 7 & 8 to use automatically detected system locale.
