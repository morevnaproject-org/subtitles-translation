#!/usr/bin/env python3
# A script for embedding the so-called multi-language srt files into supported video containers (.mkv, .mp4, .mov)
# Currently licenced under the Modified BSD license

from gettext import gettext as _
import sys
from argparse import ArgumentParser
import msrt_tool
import tempfile
import subprocess
import os.path

__version__ = '0.1'

def process_args():
    parser = ArgumentParser(description=_("Embed msrt into video files."))

    parser.add_argument("input_msrt",
        help=_("A path to the msrt file you want to embed."))

    parser.add_argument("--language", "-l",
        nargs="+",
        help=_("A list of languages that you would like to embed from the msrt file."))

    parser.add_argument("--default", "-d",
        help=_("The language to be enabled by default for video players that support this."))

    parser.add_argument("input_video",
        help=_("A path to the video file you want embed into."))

    parser.add_argument("--output", "-o",
        help=_("A path to the where you want the output video to be written to. If unspecified, input video is overwritten (changes are theoretically non-destructive)."))

    parser.add_argument("--burn", "-b",
        action="store_true",
        help=_("Burns the subtitles into the video. Ignored if there is more than one language specified. Warning: the video must be reencoded which may reduce quality."))

    parser.add_argument("--codec", "-c",
        choices=["ass", "srt", "ssa"],
        default="srt",
        help=_("Specifies the codec for the output subtitles. This is ignored unless the output file is .mkv."))

    parser.add_argument("--style", "-s",
        help=_("The style to use for burning subtitles. Follows the ASS style format. Ex: 'FontName=DejaVu Serif,PrimaryColour=&HAA00FF00'."))

    parser.add_argument("--version", "-v", action='version', version=_("msrt-embed version %s") % __version__)

    return parser.parse_args()

def main():
    args = process_args()

    # Warn and ignore if default is not in the provided langauges
    if args.default and not args.default in args.language:
        print("Warning: default language '" + args.default + "' is not in the provided list of languages, it will be ignored.")

    # Use --output argument if available, else use input_video argument
    output = args.output if args.output else args.input_video

    # Only burns subtitles if the --burn argument was specified and there is only one language
    should_burn = False
    if args.burn:
        if len(args.language) == 1:
            should_burn = True
        else:
            print("Warning: Cannot burn subtitles, more than one language provided. This argument will be ignored.")

    # Add input_video as the 0th input stream
    ffmpeg_iargs = ["ffmpeg", "-i", args.input_video]
    # Copy audio, use all streams from input_video
    ffmpeg_oargs = ["-c:a", "copy", "-strict", "experimental", "-map", "0"]
    # Only copy video if not burning subtitles
    if not should_burn:
        ffmpeg_oargs.extend(["-c:v", "copy"])
    # Set subtitle codec
    if os.path.splitext(output)[1] == ".mkv":
        if args.codec:
            ffmpeg_oargs.extend(["-c:s", args.codec])
    else:
        # mov_text is the only valic subtitle codec for mp4 and mov containers
        ffmpeg_oargs.extend(["-c:s", "mov_text"])

    # Create a temporary directory to hold intermediary .srt files
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Loop through all languages. stream_counter is the output subtitle stream number and the input stream number - 1
        for stream_counter, lang in enumerate(args.language):
            # Create srt path in temporary directory for each language
            srt_path = os.path.join(tmp_dir, lang + ".srt")
            # Extract the language lang from the .msrt input to the temporary <lang>.srt
            with open(args.input_msrt, 'r') as msrt_file, open(srt_path, 'w') as srt_file:
                msrt_tool.convert(msrt_file, srt_file, lang)
            # Add temporary <lang>.srt as an input stream as a video filter
            if should_burn:
                subfilter = "subtitles=" + srt_path
                if args.style:
                    subfilter += ":force_style='" + args.style + "'"
                ffmpeg_oargs.extend(["-vf", subfilter])
            else:
                ffmpeg_iargs.extend(["-i", srt_path])
                # Add metadata language and copy subtitle if not burning
                ffmpeg_oargs.extend(["-metadata:s:s:" + str(stream_counter), "language=" + lang, "-map", str(stream_counter+1)])
                if args.default and args.default == lang:
                    # Set the default subtitle with disposition
                    ffmpeg_oargs.extend(["-disposition:s:" + str(stream_counter), "default"])
        # Finally add the output file
        ffmpeg_oargs.append(output)
        # Print out the command and arguments for debugging purposes
        print("Running:", ffmpeg_iargs + ffmpeg_oargs)
        # Run the ffmpeg command, wait until completion, and throw and error if it has a non-zero exit status
        subprocess.run(ffmpeg_iargs + ffmpeg_oargs, check=True)

if __name__ == "__main__":
    main()
