#!/usr/bin/env python3
"""Search Pexels for portrait stock B-roll and download the matches.

usage: broll.py "search query" [OUT_DIR]

Requires PEXELS_API_KEY in the environment. Downloads up to 3 portrait clips,
prints their paths, and appends required photographer credits to
OUT_DIR/credits.txt — include those credits in the post caption.
"""
import json
import os
import sys
import urllib.parse
import urllib.request


def main():
    query = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "broll"
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        sys.exit("PEXELS_API_KEY is not set")

    params = urllib.parse.urlencode(
        {"query": query, "orientation": "portrait", "per_page": 3, "size": "medium"}
    )
    req = urllib.request.Request(
        f"https://api.pexels.com/videos/search?{params}", headers={"Authorization": key}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    os.makedirs(outdir, exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in query)[:40]
    credits_path = os.path.join(outdir, "credits.txt")
    found = 0
    with open(credits_path, "a") as credits:
        for i, video in enumerate(data.get("videos", [])):
            portrait = [f for f in video["video_files"] if f["height"] >= f["width"]]
            if not portrait:
                continue
            best = min(portrait, key=lambda f: abs(f["height"] - 1920))
            path = os.path.join(outdir, f"{slug}_{i}.mp4")
            urllib.request.urlretrieve(best["link"], path)
            credits.write(f"{path}: Video by {video['user']['name']} on Pexels ({video['url']})\n")
            print(path)
            found += 1
    if not found:
        sys.exit(f"no portrait results for: {query}")
    print(f"credits appended to {credits_path}")


if __name__ == "__main__":
    main()
