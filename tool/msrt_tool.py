#!/usr/bin/env python3
# A script for converting the so-called multi-language srt files to regular srt files
# Currently licenced under the Modified BSD license

from gettext import gettext as _
import sys
from argparse import ArgumentParser

__version__ = '0.1'

def process_args():
    parser = ArgumentParser(description=_("Convert msrt to srt files."))

    parser.add_argument("input",
            help=_("A path to the msrt file you want to convert."))

    parser.add_argument("language",
            help=_("The language to extract"))

    parser.add_argument("--output", "-o",
            action="store",
            help=_("A path to the where you want the output srt file to be written to. If unspecified, output is written to the standard output."),
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

def convert(input, output, language):
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

    with open(args.input, 'r') as input:
        try:
            if args.output == "-":
                output = sys.stdout
            else:
                output = open(args.output, 'w')

            convert(input, output, args.language)
        finally:
            if output != sys.stdout:
                output.close()

if __name__ == "__main__":
    main()
