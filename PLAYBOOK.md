# AI Clipping Playbook

What the guy in the reel is doing, how the money actually flows, and how to start
without getting banned or copyright-struck.

## What he's actually doing

His pipeline, as shown in the video:

1. Take a long-form video (podcast episode, sports show, interview).
2. Use an AI agent (he built his as a Claude "clipping skill") to find the best
   moments and cut them into vertical short-form clips with captions.
3. Have the AI overlay contextual stock footage / B-roll based on a
   second-by-second transcript, so the clips hold attention.
4. Post the clips at high volume across many niche pages.

You can replicate steps 1–3 today with the vidIQ tools connected to this
project — see `.claude/skills/clip-video/SKILL.md`. You don't need to write
the agent from scratch like he did.

## How the money actually flows (this part is NOT in the video)

Clipping makes money through a few real channels:

1. **Paid clipping programs (best way to start).** Podcasters, streamers, and
   brands pay clippers per 1,000 views, typically through marketplaces like
   Whop ("clipping" section). Rates commonly run $0.50–$2.00 per 1k views.
   This solves the two hardest problems at once: you get **permission to use
   the content** and you get **paid directly for views** without needing a
   monetized account.
2. **Direct deals with creators.** Once you can show results, offer clipping
   as a service ($500–$2,000+/mo per client is a common range for someone
   running a creator's shorts channels).
3. **Monetizing your own pages.** YouTube Shorts revenue, TikTok rewards, and
   Instagram bonuses — but all of these now require **original or meaningfully
   transformative content**. Pure repost/clip farms get excluded from payouts
   and often banned. This is the slowest and most fragile route.

## The two ways this strategy gets people wrecked

**Copyright.** Clipping a Joe Rogan episode without permission can get your
pages struck or taken down, and views on unlicensed content generally can't be
monetized. Fix: only clip content you have rights to — paid clipping programs,
creators who hired you, podcasts with official clipping programs, or your own
content.

**Spam enforcement.** "10–30 pages posting 20×/day" is exactly the pattern
Instagram and TikTok ban as coordinated inauthentic behavior. New accounts
posting at bot volume get shadowbanned fast. Fix: start with 1–3 pages,
posting 1–3 quality clips per day each, and scale only what's working.

## Week-1 plan

1. **Pick a program.** Browse Whop's clipping marketplace, pick 1–2 programs
   in a niche you actually enjoy watching (you'll be picking moments — taste
   matters).
2. **Set up 1–2 pages** on TikTok + Instagram (same handle), niche-named, with
   a clean profile.
3. **Generate your first batch.** Open this repo in a Claude session and say:
   "clip this video" with the YouTube link. The skill handles moment selection,
   B-roll suggestions, and title options. (~9 vidIQ credits per minute of
   source video — current free balance covers roughly a 9-minute source, so
   start with a short video or a segment, and top up credits when you commit
   to a program.)
4. **Post 1–3 clips/day for a week.** Submit them to the clipping program.
5. **Study what hit.** Use the vidIQ outlier tools (`vidiq_outliers`,
   `vidiq_ig_outlier_reels_search`) to see which clips in your niche
   overperform, and make more of that.

## Scaling (only after something works)

- Add pages one at a time, each with a distinct niche/angle — not 30 clones.
- Use a real scheduling tool (Later, Metricool, Buffer) instead of building
  your own like he plans to; that's a months-long detour with no revenue.
- When a program pays out reliably, reinvest in vidIQ credits — clip
  generation cost is the main variable expense.

## Honest expectations

Most clippers earn $0 in month 1 while learning what holds attention. The ones
who earn ($500–$5,000+/mo from program payouts) treat it like a reps game:
consistent daily posting, studying outliers, and iterating on hooks. The AI
pipeline removes the editing bottleneck — it does not remove the need for
judgment about what's worth clipping.
