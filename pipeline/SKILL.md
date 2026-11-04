---
name: billion-dollar-mistakes-video
description: Produce, fix or re-schedule a video for Mees's faceless YouTube channel "Billion Dollar Mistakes" (money / business / scandal stories, animated, fact-checked). Use whenever Mees asks to make a new video, change an existing one (sound, thumbnail, visuals), show/send a video or thumbnail, or schedule it on YouTube via Metricool. Contains his standing preferences and the cheap ways to do each step.
---

# Billion Dollar Mistakes — video skill

Owner: **Mees**. Always talk to him in **Dutch**, short and concrete.
Full runbook + scripts live in the GitHub repo **mees-byte/bom-media** (`pipeline/`):
`PIPELINE.md` (steps 0–11), `STYLE.md` (preferences + dated lessons), `SCHEDULE.md` (slots, evergreen queue, log),
`render.py`, `mix.py`, `thumb.py`, `pixabay.py`, `pixabay_photos.py`, `shorts.py`, and approved examples in
`pipeline/examples/binance/` and `pipeline/examples/blockbuster/`.
Start every job by cloning the repo and reading `PIPELINE.md` + `STYLE.md`. If anything here conflicts with a newer
line in `STYLE.md`, the repo wins.

## Mees's standing preferences (always apply)

1. **No whoosh/sweep sound** on scene changes or chapter cards. Only the short impact on big numbers is allowed
   (`mix.py` already does this — don't add whooshes back).
2. **Thumbnails in the same design as the video** — never AI-generated images. Build them with `pipeline/thumb.py`:
   video background, **real company logo(s) on white plates**, **WHITE text** with thick black outline,
   **gold question marks**, a curiosity question ("WHO STOLE $6.3 BILLION?"). Keep the bottom-right corner empty
   (YouTube duration). Make 2 layouts, look at both, let Mees pick when he's present.
   Approved reference: `examples/binance/thumb_spec.json` (dark layout).
3. **Visuals like the approved Binance video** ("perfect"): Pixabay **photo backgrounds** (`"px:<name>"`) behind ~2/3 of
   the scenes, 2–3 bright full-screen photo breaks (`"pxb:<name>"` + kind `photo`), 3–6 Pixabay **b-roll clips**
   (kind `broll`), chapter cards plain. Every photo must fit the claim on screen (no bitcoin coin behind an XRP or ETH
   number). No identifiable people, nothing that pretends to be footage of the real event.
   Reference: `examples/binance/scenes.py`.
4. **Real company logos**, never the company name as plain text (Wikimedia Commons SVG → PNG; download all logos first,
   ~10 s apart, Wikimedia rate-limits fast).
5. **Voice:** ElevenLabs "Arthur" `C1npRmjB19a6yNkEucvx` on `eleven_v4` with delivery tags (`[dramatically]`,
   `[intense]`, `[curious]`, `[confident]`); 480–520 words ≈ 3:15–3:30.
6. **Spend as few credits as possible.** Free: Pixabay, own rendering (ffmpeg/PIL), re-mixing audio, sending files.
   Costs credits: ElevenLabs voice (~3.3k), music (~0.9k), AI images (avoid), transcription (only for the narration —
   never to check music for vocals), vidIQ (max 1 call per trend run).
   Changing sound/thumbnail/visuals of an existing video = re-render/re-mix only, **no new voice or music**.
7. **When Mees asks to see something, send the file** (`SendUserFile`) — the video in the work dir, or the thumbnail.
   For bigger changes, show a test first and only replace the scheduled post after he approves.
8. **Fact check is sacred:** every number sourced in `FACTS.md`; independent Agent fact check before voice generation;
   never publish a fail. No Anthropic as topic, no partisan politics, no investment advice.

## Keys & accounts
- Metricool brand `blogId 7850889` (YouTube channel Billion Dollar Mistakes). Slots Mon/Wed/Fri 17:00 Europe/Amsterdam.
- **Pixabay key:** never write it into the public repo. It comes from the scheduled-task prompt (`PIXABAY_KEY`) or from
  Mees. No key → skip Pixabay visuals and say so in the final message.

## Cheap recipes for common requests
- **"Haal het geluid X eruit / pas de mix aan"** → edit `pipeline/mix.py` if it's a standing preference, re-run
  `VIDEO_DIR=work python3 bom-media/pipeline/mix.py /abs/thumb.png /abs/music.mp3` (absolute paths!), re-upload, update post.
- **"Andere thumbnail"** → new `thumb_spec.json` + `thumb.py`, re-mix (the video opens with the thumbnail for 1 s),
  re-upload video + jpg, update post.
- **"Betere visuals"** → `pixabay_photos.py` (look at `_sheet.jpg`, copy picks to `work/px/`), set `px:`/`pxb:` backgrounds
  in scenes.py, delete only the changed `scenes/sNNN.mp4`, `render.py render 2` (re-renders just those), re-mix.
- **Re-upload** → `media` branch is shared: fetch it, worktree on `origin/media`, `git rm` only your own old file,
  add the new one, normal commit + push (no force-push). Give Metricool the **commit-pinned** raw URL
  `https://raw.githubusercontent.com/mees-byte/bom-media/<sha>/<file>` and check it returns 200.
- **Update the scheduled post** → `updateScheduledPost` with the latest `id` + same `uuid`, full original info,
  only `media` (and `videoThumbnailUrl` if changed) swapped. Each update gives a new id.

## Finish every job
- Log the change in `pipeline/SCHEDULE.md`; add any new preference/lesson to `pipeline/STYLE.md`; commit + push main.
- Tell Mees in Dutch: what changed, the slot, the Metricool planner link, and the credits used (0 when nothing was generated).
