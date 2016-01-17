#!/usr/bin/python
import argparse
import os
import sys
import re
import ctypes
import struct
import json


#Helper functions
def hash_djb2(string):
    """hash a string using djb2 with seed 5381
    Args:
        string (str): string to hash
    Returns:
        (int): hashval of string masked to force positive by masking 32-bit
    """
    hashval = ctypes.c_uint(5381)
    for char in string:
        hashval.value = ((hashval.value << 5) + hashval.value) + ord(char)
    return hashval.value & 0x7FFFFFFF


def gen_str_dict(code_dir, ignore_some=False, ignore_localized=False):
    fileglob_list = []
    str_dict = {}

    pbllog_regex = "\"(?P<loc>[^\)\n]+)\""

    if ignore_some:
        pblapplog_regex = "(APP_LOG|#define|#import|#include|\/\/|snprintf).*\"(?P<loc>[^\)\n]+)\""
        pbllog_regex = ".*\"(?P<loc>[^\)\n]+)\""
    if ignore_localized:
        pbllocalized_regex = "_\(\"(?P<loc>[^\)\n]+)\"\)"

    for root, dirnames, filenames in os.walk(code_dir):
        for filename in [filename for filename in filenames if ".c" in filename[-2:]]:
            fileglob_list.append(os.path.join(root, filename))
    for filename in fileglob_list:
        if ignore_some:
            applog_locs = []
        if ignore_localized:
            localized_locs = []
        str_dict[filename] = []
        with open(filename, 'rb') as afile:
            text = afile.read()
            if ignore_some:
                applog_match_list = re.finditer(pblapplog_regex, text)
                if applog_match_list:
                    for match in applog_match_list:
                        applog_locs += [match.group('loc')]

            if ignore_localized:
                localized_match_list = re.finditer(pbllocalized_regex, text)
                if localized_match_list:
                    for match in localized_match_list:
                        localized_locs += [match.group('loc')]

            match_list = re.finditer(pbllog_regex, text)
            if match_list:
                for match in match_list:
                    text = match.group('loc')
                    push = True
                    if ignore_some and text in applog_locs:
                        applog_locs.pop(applog_locs.index(text))
                        push = False
                    if ignore_some and text in localized_locs:
                        localized_locs.pop(localized_locs.index(text))
                        push = False
                    if push:
                        str_dict[filename] += [text]
    return str_dict


def gen_loc_dict(code_dir):
    fileglob_list = []
    loc_dict = {}
    pbllog_regex = "_\(\"(?P<loc>[^\)\n]+)\"\)"

    for root, dirnames, filenames in os.walk(code_dir):
        for filename in [filename for filename in filenames
                         if ".c" in filename[-2:]]:
            fileglob_list.append(os.path.join(root, filename))
    for filename in fileglob_list:
        with open(filename, 'rb') as afile:
            text = afile.read()
            match_list = re.finditer(pbllog_regex, text)
            if match_list:
                for match in match_list:
                    loc_dict[hash_djb2(match.group('loc'))] = match.group('loc')

    return loc_dict


def main():
    parser = argparse.ArgumentParser(description='Generate locale dicts.')
    parser.add_argument('source', metavar='SRC',
                        help='source folder (try ./src)')
    parser.add_argument('output', metavar='OUTPUT',
                        help='output JSON file (eg loc_english.json)')
    parser.add_argument('-p', '--purge', help='Overwrite the output dictionary', action='store_true')

    args = parser.parse_args()

    code_dir = args.source
    output_filename = args.output

    str_dict = gen_str_dict(code_dir, True, True)

    hash_dict = gen_loc_dict(code_dir)

    print("== Unlocalized strings (ignoring applog, comments, defines, includes, snprintf) ==")
    for key, item in str_dict.iteritems():
        values = [string for string in item]
        if len(values) > 0:
            print(key)
            for string in values:
                print('    ' + string)
    print("==================================================================================")

    if not args.purge:
        data = {}
        if os.path.isfile(output_filename):
            data = json.load(open(output_filename, "r"))

        for key, value in hash_dict.iteritems():
            if str(key) in data.keys():
                hash_dict[key] = data[str(key)]

        json.dump(hash_dict, open(output_filename, "wb"), indent=2, sort_keys=True)
    else:
        json.dump(hash_dict, open(output_filename, "wb"), indent=2, sort_keys=True)

    print("%s now has %d entries\n" % (output_filename, len(hash_dict)))

    #create binary resource loadable as a pebble dictionary
    with open(output_filename.replace('.json', '.bin'), 'wb') as output_bin:
        output_bin.write(struct.pack('I', len(hash_dict)))  # count of entries
        for (key, value) in hash_dict.iteritems():
            output_bin.write(struct.pack('I', key))  # key
            output_bin.write(struct.pack('I', len(value) + 1))  # length of string including null
            output_bin.write(value)  # write string as c string
            output_bin.write(struct.pack('B', 0))  # null terminate string


    #output tuple array
    #with open(output_filename + '.bin', 'wb') as output_bin:
      #dump the tuple header for the dictionary
    #  output_bin.write(struct.pack('B', len(hash_dict))) #count of items
    #  for (key, value) in hash_dict.iteritems():
    #    output_bin.write(struct.pack('I',key)) #key
    #    output_bin.write(struct.pack('b',1)) #type cstring
    #    output_bin.write(struct.pack('<H',len(value) + 1)) #length of string including null
    #    output_bin.write(value) #write string as c string
    #    output_bin.write(struct.pack('B',0)) #null terminate string


if __name__ == '__main__':
    main()
