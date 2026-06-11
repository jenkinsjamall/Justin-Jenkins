#!/usr/bin/env python3
"""Burn an .srt caption file into a clip (run last, after overlays).

usage: caption.py CLIP SRT OUT

Avoid spaces or special characters in the SRT path; the ffmpeg subtitles
filter parses it.
"""
import subprocess
import sys

STYLE = (
    "FontName=DejaVu Sans,FontSize=15,Bold=1,PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=70"
)


def main():
    clip, srt, out = sys.argv[1:4]
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", clip,
            "-vf", f"subtitles={srt}:force_style='{STYLE}'",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "copy",
            out,
        ],
        check=True,
    )
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
