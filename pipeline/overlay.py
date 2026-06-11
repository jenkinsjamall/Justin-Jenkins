#!/usr/bin/env python3
"""Overlay full-frame B-roll onto a vertical clip at given timestamps.

usage: overlay.py CLIP OUT BROLL.mp4:START:DURATION [BROLL2.mp4:START:DURATION ...]

START/DURATION are seconds within CLIP. Each B-roll is scaled/cropped to
1080x1920 and shown full-frame for DURATION while the clip's audio continues.
Keep overlays 2-4s and never cover the opening hook line.
"""
import subprocess
import sys


def main():
    clip, out = sys.argv[1], sys.argv[2]
    specs = []
    for spec in sys.argv[3:]:
        path, start, dur = spec.rsplit(":", 2)
        specs.append((path, float(start), float(dur)))
    if not specs:
        sys.exit("no B-roll specs given")

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", clip]
    filters = []
    last = "[0:v]"
    for i, (path, start, dur) in enumerate(specs, start=1):
        cmd += ["-i", path]
        filters.append(
            f"[{i}:v]trim=0:{dur},scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,setpts=PTS-STARTPTS+{start}/TB[b{i}]"
        )
        filters.append(
            f"{last}[b{i}]overlay=enable='between(t,{start},{start + dur})':eof_action=pass[v{i}]"
        )
        last = f"[v{i}]"
    cmd += [
        "-filter_complex", ";".join(filters),
        "-map", last, "-map", "0:a?", "-c:a", "copy",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        out,
    ]
    subprocess.run(cmd, check=True)
    print(f"wrote {out} with {len(specs)} B-roll overlay(s)")


if __name__ == "__main__":
    main()
