# Billion Dollar Mistakes — automatic production runbook

You are producing ONE long video (and sometimes one Short) for the faceless YouTube channel
**Billion Dollar Mistakes** (English, money / business / scandal stories, animated, fact-checked).
The owner (Mees, Dutch-speaking) does not review videos. Work fully on your own, but never publish
anything that fails the fact check. Talk to the owner in **Dutch**.

## 0. Start
1. Attach and clone the repo: `add_repo` owner `mees-byte`, repo `bom-media`, access `push`; clone to `/home/claude/bom-media`.
2. Read `pipeline/STYLE.md` (lessons, always apply) and `pipeline/SCHEDULE.md` (evergreen queue + log).
3. Work out the slot: the next Mon/Wed/Fri at **17:00 Europe/Amsterdam** that has no entry in the SCHEDULE log.
   Wednesday = evergreen (first open item in the queue). Monday/Friday = trend.
4. **Send the owner a message first (SendUserMessage, Dutch):**
   `🎬 Nieuwe video wordt nu gemaakt en gerenderd voor <dag datum> 17:00 — onderwerp: <onderwerp>.`

## 1. Topic (trend slots)
- vidIQ `vidiq_keyword_research` mode `rising`, niche "business scandals, company collapses, stock market, billionaires", period week;
  plus WebSearch for the biggest business/markets news of the last 48 hours.
- Pick a story with a clear conflict, a big number and a twist. Check search demand.
- Never: Anthropic (we can't be independent), partisan/election politics, personal investment advice, unconfirmed allegations.
- Don't repeat a topic from the SCHEDULE log within 8 weeks.

## 2. Research → `work/FACTS.md`
Every number and claim with a source (link + date). Prefer primary/major sources. If it can't be sourced, it doesn't go in.

## 3. Packaging + script (handbook framework)
- 5 titles (search keyword up front, concrete number, true), 3 thumbnail concepts, 3 double hooks scored → pick best.
- Script **480–520 words** (Arthur on eleven_v4 ≈ 3:15–3:30). Hook 1 0–3 s, hook 2 before 8 s, promise before 15 s.
  Chapters with tease + re-hook, 3–5 open loops all closed, twist halfway, comment question with two sides right after
  the dilemma, one value subscribe line at 60–75 %, callback ending.
- Add eleven_v4 delivery tags where the mood changes: `[dramatically]`, `[confident]`, `[intense]`, `[curious]`, `[excited]`.
  CAPS on 1 key word per few sentences for emphasis. Numbers spelled as words.
- Save `work/NARRATION.txt` (with tags) and `work/SCRIPT.md` (packaging, hooks, chapter plan, pinned comment).

## 4. Fact check (BEFORE spending voice credits)
Spawn an Agent (general-purpose) that gets FACTS.md + NARRATION.txt, checks every claim against the sources (WebFetch),
and returns PASS or a list of problems. Fix and re-check. If it still fails twice: do not publish; message the owner (Dutch) why,
and pick the next evergreen instead.

## 5. Voice
- ElevenLabs `creative_generate_speech`: model `eleven_v4`, voice_id `C1npRmjB19a6yNkEucvx` (Arthur), generations_count 1, prompt = NARRATION.txt.
- Poll `creative_get_flow_run_status`, download `content_url` to `work/voice.mp3` (curl).
- `creative_transcribe_audio` model `eleven_scribe_v1`, flow_id of the speech, connect_from = speech node_id. Download `words_download_url`,
  drop entries whose text starts with `[` or is `—`, save as `work/words.json` = `{"words":[...]}`.

## 6. Scenes → `work/scenes.py`
- One `sc("first words of the sentence", "kind", "bg", **args)` per new image; anchors must match the transcript words in order.
- Scene ≤ 4.5 s, a pattern break (chapter card / colour bg / big word) at least every 20 s, a different animation per key claim.
- Kinds in `render.py`: title, count, date, offer, store, stores_grid, pie, envelope, loss, people, quote, chapter, timeline, access,
  checkmate, subs, question, bonus, comment, subscribe. Backgrounds: dark, blue, red, gold, green.
  Use `examples/blockbuster/scenes.py` as the style reference. You may define new `def k_name(img, t, dur, a)` kinds inside scenes.py
  (they are registered automatically) — make at least 3 story-specific ones per video ("every video 5 % better").
- **Real company logos, never the name as plain text**: download from Wikimedia Commons (upload.wikimedia.org original SVG via the
  md5 path, User-Agent set, 2 s between requests; render with `rsvg-convert -w 1200`) to `work/logos/<name>.png`; use `logo="name"`
  (title/count/people) and `plate=(250,250,252)` on coloured backgrounds. Existing in `pipeline/logos/`: netflix, blockbuster, seveneleven.
- Never draw invented chart data. Never show photos of real people (use the generic person card).

## 7. Render + check
```
VIDEO_DIR=work python3 bom-media/pipeline/render.py preview 3@1.5 10@2 ...   # check 6+ busy frames with Read
VIDEO_DIR=work python3 bom-media/pipeline/render.py render 2
```
Check: no text outside the frame or under the captions (keep content above y≈900), numbers correct, logos visible.

## 8. Thumbnail + music
- ElevenLabs `creative_generate_image`, model `gpt-image-2`, 2 variations, prompt from the handbook template
  (one subject + emotion, 2–3 words huge yellow with thick black outline top-left, bottom-right 15 % empty, no real people's faces,
  no fake logos). Pick the best, save as `work/thumb.png` and a JPG ≤ 2 MB.
- New music each video: `creative_generate_in_flow` node_type `music`, model `eleven_music_v2_5`, generations_count 1,
  "Instrumental only, no vocals … documentary underscore … sits under narration, ~3 minutes" with a mood that fits the story.
  Download to `work/music.mp3`.
- `VIDEO_DIR=work python3 bom-media/pipeline/mix.py work/thumb.png work/music.mp3` → `work/VIDEO.mp4` (thumbnail opens the video for 1 s).
- Sample 12 frames from VIDEO.mp4 into a contact sheet and look at it before uploading.

## 9. Upload (Metricool, brand blogId `7850889`, YouTube channel UCy4RTiZ57S2HfvPEiRJ2Y3Q)
1. Host the files on the throw-away branch `media` (one commit, force-pushed, so main never grows):
   ```
   cd /home/claude && rm -rf media && mkdir media && cp work/VIDEO.mp4 media/<date>-<slug>.mp4 && cp work/thumb.jpg media/<date>-<slug>.jpg
   cd media && git init -q -b media && git add . && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "media <date>" \
     && git push -f https://github.com/mees-byte/bom-media media
   ```
   Public URL: `https://raw.githubusercontent.com/mees-byte/bom-media/media/<file>` (check it returns 200 with curl).
2. `createScheduledPost` with date `<slot>T17:00:00+01:00` (or +02:00 in summer time) and info JSON exactly like
   `examples/blockbuster/post_info.json`: autoPublish true, providers youtube, youtubeData {title (A), type video, privacy public,
   tags (≤ 490 chars total), category EDUCATION, madeForKids false, isAiGeneratedContent false}, videoThumbnailUrl,
   text = long SEO description (≥ 1,500 chars: hook sentences, "In this animated explainer…", What you'll learn, Sources, Chapters
   from the chapter scene times + 1 s, "Not financial advice. For education only.", credits, exactly 3 hashtags).
   If the thumbnail is rejected (VIDEO_THUMBNAIL_NOT_APPLICABLE), retry once without videoThumbnailUrl.
3. Metricool copies the media to its own storage (the response shows static.metricool.com URLs). Nothing to clean up — the next run overwrites the `media` branch.

## 10. Short (only in the Sunday and Tuesday runs, i.e. for Monday/Wednesday videos)
- Metricool free plan = 20 posts per calendar month. Count this month's posts with `getScheduledPosts` + the SCHEDULE log;
  only make the Short if fewer than 19 are used.
- `python3 bom-media/pipeline/shorts.py work/VIDEO.mp4 <start> <20–30 s> "<hook ≤ 6 words>" work/short.mp4` — pick the strongest
  "what does this mean for YOUR money" or twist moment. Schedule as youtube type `short` the day after the long video at 17:00,
  title with #shorts, text ending with the long video title.

## 11. Finish
- Append to `pipeline/SCHEDULE.md` log: date, slot, title, topic, Metricool plannerUrl, credits used. Commit + push (never commit work/).
- **Message the owner (Dutch)**: `✅ Ingepland: "<titel>" — <dag datum> 17:00. Thumbnail + link: <plannerUrl>`.
- Any error you cannot fix: message the owner what failed and what you did instead. Never skip a slot silently.
