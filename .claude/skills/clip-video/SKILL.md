---
name: clip-video
description: Turn a long-form video into short vertical clips with captions and contextual B-roll overlays using the DIY pipeline in pipeline/ (yt-dlp, faster-whisper, ffmpeg, Pexels). Use when the user asks to clip a video, make shorts/reels, or run the clipping pipeline.
---

# Clip a long-form video into shorts (DIY pipeline)

Free, unlimited pipeline — no vidIQ credits. Helper scripts live in
`pipeline/`. Work in a scratch dir like `/tmp/clips/<video-slug>/`.

## 0. Pre-flight

1. Ensure tools: run `scripts/install_pipeline.sh` if `ffmpeg` or
   `yt-dlp`/`faster-whisper` are missing (a SessionStart hook normally does
   this).
2. Check `PEXELS_API_KEY` is set (environment variable from the cloud
   environment settings).
3. Check network: `curl -s -o /dev/null -w "%{http_code}"` against
   `https://www.youtube.com`, `https://api.pexels.com`, and
   `https://huggingface.co`. If any return 403 with header
   `x-deny-reason: host_not_allowed`, tell the user to add the missing hosts
   to the environment's Custom network allowlist (`www.youtube.com`,
   `*.youtube.com`, `*.googlevideo.com`, `*.pexels.com`, `api.pexels.com`,
   `huggingface.co`, `*.huggingface.co`, `*.hf.co`) and start a fresh
   session. Only fall back to the vidIQ MCP tools (`vidiq_generate_clips`,
   `vidiq_generate_broll`) if the user agrees to spend credits.
4. Confirm the user has rights to clip the content (their own, a clipping
   program's, or a client's). Ask before proceeding if unclear.

## 1. Download the source

```
yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o source.mp4 <URL>
```

## 2. Transcribe

```
python3 pipeline/transcribe.py source.mp4 transcript.json
```

First run downloads the Whisper model (~75MB) from Hugging Face. A 1-hour
episode takes several minutes on CPU — start it early.

## 3. Pick moments (this is the judgment step — do it well)

Read `transcript.json` and choose 30–45s windows that work as standalone
clips. Use the user's steer (e.g. "funniest parts") if given. Favor:
- A strong first line that works as a hook out of context.
- Self-contained stories, hot takes, debates, punchlines.
- Clean start/end boundaries on sentence edges (snap to word timestamps).

Propose 3–5 moments with timestamp ranges and a one-line rationale each.

## 4. Cut each clip

```
python3 pipeline/cut.py source.mp4 transcript.json START END clipN.mp4
```

Produces a 1080x1920 center-cropped clip plus `clipN.srt` (captions timed to
the clip). Note: center-crop suits single-speaker framing; for off-center
speakers, adjust the crop filter manually.

## 5. B-roll (the mechanic from the reel)

For each clip, derive 2–3 concrete, visual search terms from what's being
said in that segment (e.g. someone describing a dunk → "basketball player
dunking"). Then:

```
python3 pipeline/broll.py "search query" broll/
python3 pipeline/overlay.py clipN.mp4 clipN_b.mp4 broll/file.mp4:START:3 [...]
```

START is seconds within the clip. Keep overlays 2–4s, max ~1 per 10s, and
never cover the opening hook line. `broll/credits.txt` accumulates required
Pexels attributions — they must go in the post caption.

## 6. Burn captions (always last, on top of overlays)

```
python3 pipeline/caption.py clipN_b.mp4 clipN.srt clipN_final.mp4
```

## 7. Deliver

Send the final clips with SendUserFile. For each clip include: source
timestamp range, suggested hook/title, a ready-to-paste caption with 3–5
niche hashtags plus the Pexels credits, and any clipping-program
requirements the user mentioned (watermarks, creator tags).

## 8. Optional research add-ons (vidIQ, cheap)

- `vidiq_outliers` / `vidiq_ig_outlier_reels_search` — find overperforming
  shorts in the niche before picking moments.
- `vidiq_generate_titles` / `vidiq_score_title` — title and hook options.
- `vidiq_keyword_research` — caption keywords/hashtags.
