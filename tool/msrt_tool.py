#!/usr/bin/env python3
# A script for converting the so-called multi-language srt files to regular srt files
# Licenced under the Modified BSD license

# Extract language to given SRT:
#    msrt_tool.py MSRT_FILE extract LANG [SRT_FILE]
# Merge given SRT file to specified language (not implemented yet):
#    msrt_tool.py MSRT_FILE merge LANG SRT_FILE
# List languages available in msrt file (not implemented yet):
#    msrt_tool.py MSRT_FILE list

from gettext import gettext as _
import sys
from argparse import ArgumentParser

__version__ = '0.2'

def process_args():
    parser = ArgumentParser(description=_("A tool for working with MSRT (multilanguage SRT) subtitle files."))

    parser.add_argument("msrtfile",
            help=_("A path to the msrt file."))

    parser.add_argument("action",
            help=_("Action: 'extract'."))

    parser.add_argument("language",
            help=_("Language code."),
            default="")

    parser.add_argument("srtfile",
            action="store",
            help=_("SRT file. If unspecified, output is written to the standard output."),
            default="-")

    parser.add_argument("--version", "-v", action='version', version=_("msrt_tool version %s") % __version__)

    return parser.parse_args()


class MsrtFile():
    def __init__(self, path, language=None):
        self._data = {}

        self._load(path, language)

        # self._data["00:00:01,030 --> 00:00:03,530"] = {}
        # self._data["00:00:01,030 --> 00:00:03,530"]["en"] = "English"
        # self._data["00:00:01,030 --> 00:00:03,530"]["ru"] = "Russian Text"

    def _load(self, path, language):
        with open(path, 'r') as input:
            subGroup = ""
            for line in input:
                # print(line, end='')
                if line.lstrip().startswith("[*]"):
                    # Ignore comments
                    # print("Ignore")
                    pass
                elif line == "\n":
                    # print("Done")
                    # A blank line marks the end of a subgroup, time to parse!

                    self._parse_subgroup(subGroup, language)
                    subGroup = ""
                else:
                    # print("Add")
                    # Line is part of the current subgroup
                    subGroup += line
            self._parse_subgroup(subGroup, language)



    def write_msrt(self, path):

        if path == "-":
            output = sys.stdout
        else:
            output = open(path, 'w')

        index = 1
        for key in sorted(self._data):
            if self._data[key]:
                output.write(str(index) + "\n")
                output.write(key + "\n")
                for language in sorted(self._data[key]):
                    output.write("[" + language + "] " + self._data[key][language] + "\n")
                index += 1

    def write_srt(self, path, language):

        if path == "-":
            output = sys.stdout
        else:
            output = open(path, 'w')

        index=1
        for key in sorted(self._data):
            if self._data[key] and language in self._data[key]:
                output.write(str(index)+"\n")
                output.write(key+"\n")
                output.write(self._data[key][language] + "\n")
                index+=1

    def _parse_subgroup(self, subGroup, language):
        if not subGroup:
            return
        subGroup = subGroup.split("\n")

        timerange = subGroup[1].strip()
        self._data[timerange] = {}


        for l in subGroup[2:]:
            if not language:
                # We are parsing msrt file, so let's split lines to languages
                a=l.find("[")
                b=l.find("]")
                if (a!=-1 and b!=-1):
                    linelang = l[a+1:b]
            else:
                linelang = language
            if linelang:
                if not linelang in self._data[timerange]:
                    self._data[timerange][linelang] = ""
                self._data[timerange][linelang] += l[2 + len(linelang):].strip() + "\n"

def main():
    args = process_args()

    if args.action == 'extract':
        msrt = MsrtFile(args.msrtfile)
        msrt.write_srt(args.srtfile, args.language)

    elif args.action == 'merge':
        print("Not implemented.")

    elif args.action == 'list':
        print("Not implemented.")

if __name__ == "__main__":
    main()
