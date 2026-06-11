#!/usr/bin/env python3
"""Cut a vertical 9:16 clip from a source video and write a matching .srt.

usage: cut.py SOURCE TRANSCRIPT_JSON START END OUT_MP4

START/END are seconds in the source video. Produces OUT_MP4 (1080x1920,
center-cropped) plus an .srt beside it with caption cues timed relative to
the clip, grouped a few words per cue. Burn the captions LAST with
caption.py, after any B-roll overlays.
"""
import json
import subprocess
import sys


def fmt(t):
    ms = int(round(max(t, 0) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(transcript, start, end, path, group=3):
    words = [
        w
        for seg in transcript["segments"]
        for w in seg.get("words", [])
        if start <= w["s"] < end
    ]
    cues = []
    if words:
        for i in range(0, len(words), group):
            chunk = words[i : i + group]
            cues.append(
                (chunk[0]["s"] - start, min(chunk[-1]["e"], end) - start,
                 " ".join(w["w"] for w in chunk))
            )
    else:  # transcript without word timestamps: fall back to whole segments
        for seg in transcript["segments"]:
            if start <= seg["start"] < end:
                cues.append((seg["start"] - start, min(seg["end"], end) - start, seg["text"]))
    with open(path, "w") as f:
        for n, (s, e, text) in enumerate(cues, 1):
            f.write(f"{n}\n{fmt(s)} --> {fmt(e)}\n{text.upper()}\n\n")
    return len(cues)


def main():
    src, tpath, start, end, out = sys.argv[1:6]
    start, end = float(start), float(end)
    with open(tpath) as f:
        transcript = json.load(f)
    srt = out.rsplit(".", 1)[0] + ".srt"
    cues = build_srt(transcript, start, end, srt)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", str(start), "-to", str(end), "-i", src,
            "-vf", "crop=min(iw\\,ih*9/16):ih,scale=1080:1920",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            out,
        ],
        check=True,
    )
    print(f"wrote {out} ({end - start:.1f}s) and {srt} ({cues} cues)")


if __name__ == "__main__":
    main()
