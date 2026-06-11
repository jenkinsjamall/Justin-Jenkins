---
name: clip-video
description: Turn a long-form video (YouTube link or hosted file) into short vertical clips with B-roll suggestions, titles, and posting metadata using the vidIQ MCP tools. Use when the user asks to clip a video, make shorts/reels from a video, or run the clipping pipeline.
---

# Clip a long-form video into shorts

Run this pipeline using the vidIQ MCP tools (`mcp__*__vidiq_*`). Load tool
schemas with ToolSearch first if they aren't loaded.

## 0. Pre-flight

1. Call `vidiq_balance`. Clip generation costs **9 credits per minute of
   source video, rounded up**. If the source video is longer than
   `totalCredits / 9` minutes, STOP and tell the user the cost before
   proceeding — suggest a shorter video or a segment instead.
2. Confirm the user has rights to clip this content (their own video, a
   clipping-program video, or a client's). If it's clearly third-party content
   with no permission mentioned, ask before spending credits.

## 1. Generate clips

Call `vidiq_generate_clips` with:
- `videoUrl` for a YouTube link (duration is fetched automatically), or
  `uploadedVideoUrl` + `videoDuration` + `videoFilename` for a hosted file.
- `prompt`: steer moment selection from the user's intent (e.g. "funniest
  exchanges", "hot takes and debates", "actionable advice moments").
- `clipDuration`: default to 30–45s for Reels/TikTok unless the user
  specifies.

This is async — it returns an `mcpJobId`. Poll `vidiq_job_poll` with that id
until status is `completed` (failures auto-refund credits). Do not use Bash
sleep loops; poll the tool directly between other work.

## 2. Enhance each clip

For each generated clip:
1. **B-roll:** identify 2–3 concrete visual subjects from the clip's
   transcript/topic and call `vidiq_generate_broll` with
   `orientation: "portrait"` for each. Give the user the mp4 links and the
   required photographer attribution for every clip they use.
2. **Titles/hooks:** call `vidiq_generate_titles` for title and hook-text
   options; optionally `vidiq_score_title` on the user's favorite.

## 3. Assemble B-roll overlays (when network access allows)

The B-roll mechanic from the original reel: derive search terms from what's
being said in each transcript segment, fetch matching stock clips, and overlay
them at those exact timestamps.

1. Check host access first: `curl -s -o /dev/null -w "%{http_code}" https://videos.pexels.com`.
   If 403 with `x-deny-reason: host_not_allowed`, the environment's network
   policy blocks downloads — tell the user to allow `*.pexels.com` (and
   `www.youtube.com` + `*.googlevideo.com` for source downloads) in their
   Claude Code environment settings, then deliver links-only (step 4).
2. Install ffmpeg if missing (`apt-get update && apt-get install -y ffmpeg`).
3. Download clip + B-roll mp4s with curl, then overlay each B-roll segment
   full-frame at its timestamp, keeping the original audio:
   ```
   ffmpeg -i clip.mp4 -i broll1.mp4 -filter_complex \
     "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=0:3,setpts=PTS+START/TB[b1]; \
      [0:v][b1]overlay=enable='between(t,START,START+3)'" \
     -map 0:a -c:a copy out.mp4
   ```
   (Replace START with the transcript timestamp; chain more overlay pairs for
   additional B-roll. 2–4 second overlays, never covering the hook line.)
4. Add the Pexels photographer credit for every clip used to the caption text.

## 4. Deliver

Present results as a table per clip: timestamp range in the source, clip link,
suggested hook/title, B-roll links + credits, and a suggested caption with
3–5 niche hashtags. Remind the user of any program-specific requirements
(watermarks, creator tags) if they mentioned a clipping program.

## 5. Optional research add-ons

- `vidiq_outliers` / `vidiq_ig_outlier_reels_search` — find overperforming
  shorts in the niche to steer the selection `prompt` before generating.
- `vidiq_keyword_research` — hashtag/keyword ideas for captions.
- `vidiq_video_transcript` — pull a transcript first if the user wants to
  pick moments manually before spending generation credits.
