#!/usr/bin/env python3
"""Transcribe a video/audio file to JSON with word-level timestamps.

usage: transcribe.py SOURCE [OUT_JSON]

Output JSON: {"language", "duration", "segments": [{"start", "end", "text",
"words": [{"w", "s", "e"}]}]}. Uses faster-whisper's base model on CPU.
"""
import json
import sys

from faster_whisper import WhisperModel


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "transcript.json"
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(src, word_timestamps=True)
    data = {"language": info.language, "duration": round(info.duration, 2), "segments": []}
    for seg in segments:
        data["segments"].append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
            "words": [
                {"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)}
                for w in (seg.words or [])
            ],
        })
    with open(out, "w") as f:
        json.dump(data, f)
    print(f"wrote {out}: {len(data['segments'])} segments, {data['duration']}s, lang={data['language']}")


if __name__ == "__main__":
    main()
