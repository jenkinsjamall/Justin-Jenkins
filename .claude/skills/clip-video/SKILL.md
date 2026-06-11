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

## 3. Deliver

Present results as a table per clip: timestamp range in the source, clip link,
suggested hook/title, B-roll links + credits, and a suggested caption with
3–5 niche hashtags. Remind the user of any program-specific requirements
(watermarks, creator tags) if they mentioned a clipping program.

## 4. Optional research add-ons

- `vidiq_outliers` / `vidiq_ig_outlier_reels_search` — find overperforming
  shorts in the niche to steer the selection `prompt` before generating.
- `vidiq_keyword_research` — hashtag/keyword ideas for captions.
- `vidiq_video_transcript` — pull a transcript first if the user wants to
  pick moments manually before spending generation credits.
