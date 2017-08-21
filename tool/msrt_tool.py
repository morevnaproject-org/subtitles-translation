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

    group = parser.add_mutually_exclusive_group()

    group.add_argument("--extract",
            help=_("Creates an srt file for the specified language."),
            nargs=2,
            metavar=("LANG", "SRT_FILE"))

    group.add_argument("--merge",
            help=_("Writes srt data to the specified language in the msrt."),
            nargs=2,
            metavar=("LANG", "SRT_FILE"))

    group.add_argument("--list",
            help=_("Lists languages in msrt file."),
            action="store_true")

    parser.add_argument("--version", "-v", action='version', version=_("msrt_tool version %s") % __version__)

    return parser.parse_args()


class MsrtFile():
    def __init__(self, path, language=None):
        self._data = {}
        self._comments=""

        self.load(path, language)

        # self._data["00:00:01,030 --> 00:00:03,530"] = {}
        # self._data["00:00:01,030 --> 00:00:03,530"]["en"] = "English"
        # self._data["00:00:01,030 --> 00:00:03,530"]["ru"] = "Russian Text"

    def load(self, path, language):
        with open(path, 'r') as input:
            subGroup = ""
            for line in input:
                # print(line, end='')
                if line.lstrip().startswith("[*]"):
                    # Comments
                    line = line[3:]
                    if line[0] == " ":
                        line = line[1:]
                    self._comments += line
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



    def write_msrt(self, output):
        if isinstance(output, str):
            if output == "-":
                output = sys.stdout
            else:
                with open(output, 'w') as arg:
                    return self.write_msrt(arg)

        # Comments
        if self._comments.strip():
            for line in self._comments.strip().split("\n"):
                line = "[*] " + line
                output.write(line.strip() + "\n")
            output.write("\n")

        index = 1
        for key in sorted(self._data):
            if self._data[key]:
                output.write(str(index)+"\n")
                output.write(key+"\n")
                for language in sorted(self._data[key]):
                    text = self._data[key][language].strip()
                    output.write("[" + language + "] " + text+"\n")
                index += 1
                output.write("\n")

    def write_srt(self, output, language):
        if isinstance(output, str):
            if output == "-":
                output = sys.stdout
            else:
                with open(output, 'w') as arg:
                    return self.write_srt(arg, language)

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
        if not timerange in self._data:
            self._data[timerange] = {}

        if language:
            # This means we are loading srt file, so it will get override all data for specified language
            self._data[timerange][language]=""


        for l in subGroup[2:]:
            if not language:
                # We are parsing msrt file, so let's split lines to languages
                a=l.find("[")
                b=l.find("]")
                if (a!=-1 and b!=-1):
                    language = l[a+1:b]
                if language:
                    if not language in self._data[timerange]:
                        self._data[timerange][language] = ""
                    self._data[timerange][language] += l[2 + len(language):].strip() + "\n"
                language=None
            else:
                # We are parsing  srt
                if not language in self._data[timerange]:
                    self._data[timerange][language] = ""
                self._data[timerange][language] += l.strip() + "\n"

def main():
    args = process_args()

    msrt = MsrtFile(args.msrtfile)

    if args.extract:
        msrt.write_srt(args.extract[1], args.extract[0])

    elif args.merge:
        msrt.load(args.merge[1],args.merge[0])
        msrt.write_msrt(args.msrtfile)

    elif args.list:
        print("Not implemented.")

if __name__ == "__main__":
    main()
