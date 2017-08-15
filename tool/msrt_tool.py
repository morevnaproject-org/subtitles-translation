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

__version__ = '0.1'

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

def parse_subgroup(subGroup, language):
    if not subGroup:
        return ""
    groupLines = subGroup.split("\n")

    subGroup = ""

    index = int(groupLines[0])

    startTime, endTime = groupLines[1].split("-->")
    startTime = startTime.strip()
    endTime = endTime.strip()

    langText = ""
    for l in groupLines[2:]:
        if l and l.startswith("[" + language + "]"):
            langText += l[2+len(language):].strip() + "\n"

    if langText:
        return (str(index) + "\n" +
            startTime + " --> " + endTime + "\n" +
            langText +
            "\n")
    return ""

def action_extract(input, output, language):
    subGroup = ""
    for line in input:
        #print(line, end='')
        if line.lstrip().startswith("[*]"):
            # Ignore comments
            #print("Ignore")
            pass
        elif line == "\n":
            #print("Done")
            # A blank line marks the end of a subgroup, time to parse!

            output.write(parse_subgroup(subGroup, language))
            subGroup = ""
        else:
            #print("Add")
            # Line is part of the current subgroup
            subGroup += line
    output.write(parse_subgroup(subGroup, language))

def main():
    args = process_args()

    if args.action == 'extract':
        with open(args.msrtfile, 'r') as input:

            if args.srtfile == "-":
                output = sys.stdout
            else:
                output = open(args.srtfile, 'w')

            try:
                action_extract(input, output, args.language)
            finally:
                if output != sys.stdout:
                    output.close()

    elif args.action == 'merge':
        print("Not implemented.")

    elif args.action == 'list':
        print("Not implemented.")

if __name__ == "__main__":
    main()
