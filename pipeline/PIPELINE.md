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
- **vidIQ credits are scarce (150/month, free plan). Budget: at most ONE vidIQ call per trend run, zero in evergreen (Wednesday) runs.**
  First call `vidiq_balance` (free). Only if `totalCredits` ≥ 30: one `vidiq_keyword_research` mode `rising`, niche
  "business scandals, company collapses, stock market, billionaires", period week. Below 30: skip vidIQ (the weekly review needs it).
- Always: WebSearch for the biggest business/markets news of the last 48 hours, and check search demand by WebSearch / YouTube
  search suggestions instead of extra vidIQ calls. Never use other paid vidIQ tools (titles, thumbnails, scripts, scoring) in this pipeline.
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

## 6b. B-roll from Pixabay (free, no credits)
- Key: `PIXABAY_KEY` comes from the scheduled-task prompt / owner — NEVER write it into this public repo. No key → skip b-roll, mention it in the final message.
- 4–6 clips per video, mood only (server room, code on screen, vault, stock ticker screen, city at night, ice…), matched to the chapter:
  `PIXABAY_KEY=… VIDEO_DIR=work python3 bom-media/pipeline/pixabay.py "<terms>" <name> 5` → `work/broll/<name>.mp4` (+ credits.txt).
- Use in scenes.py: `sc("anchor", "broll", "dark", clip="<name>", kicker="…", lines=["…", ("…", GOLD)])` (dim=0.35 default).
  B-roll is a pattern break: max ~4 s each, never two in a row, never on a key number/claim (those stay animated).
- LOOK at one preview frame per clip: no identifiable people, no fake logos/brands, nothing that pretends to be footage of the real event.
- Add "Stock footage: Pixabay" to the description credits line.

## 6c. Photo backgrounds from Pixabay (free, no credits)
- `PIXABAY_KEY=… VIDEO_DIR=work python3 bom-media/pipeline/pixabay_photos.py '[["name","search terms"], …]'` (~15–20 queries matched to the story:
  money, the industry's objects, city, boardroom, clock, closed sign, chess, charts…) → look at `work/px_dl/_sheet.jpg`, copy the best to `work/px/<name>.jpg`.
- In scenes.py set the background of most animation scenes to `"px:<name>"`; use `"pxb:<name>"` + kind `photo` (lines=[…], y=…, optional logo) for 2–3 bright pattern breaks.
  Keep the plain coloured backgrounds for chapter cards and a few scenes for rhythm. First scene: a bright photo.
- Add "Photos & stock footage: Pixabay" to the description credits line.

## 7. Render + check
```
VIDEO_DIR=work python3 bom-media/pipeline/render.py preview 3@1.5 10@2 ...   # check 6+ busy frames with Read
VIDEO_DIR=work python3 bom-media/pipeline/render.py render 2
```
Check: no text outside the frame or under the captions (keep content above y≈900), numbers correct, logos visible.

## 8. Thumbnail + music
- Thumbnail in the SAME design as the video (owner request 2026-11-04 — no AI images): write `work/thumb_spec.json`
  and run `VIDEO_DIR=work python3 bom-media/pipeline/thumb.py work/thumb_spec.json` (see the docstring for the format).
  Real company logo(s) on white plates, WHITE text with black outline, gold question marks, a question/curiosity line,
  bottom-right corner empty. Make 2 layouts, look at both with Read, pick the best. Costs no credits.
- New music each video: `creative_generate_in_flow` node_type `music`, model `eleven_music_v2_5`, generations_count 1,
  "Instrumental only, no vocals … documentary underscore … sits under narration, ~3 minutes" with a mood that fits the story.
  Download to `work/music.mp3`.
- `VIDEO_DIR=work python3 bom-media/pipeline/mix.py work/thumb.png work/music.mp3` → `work/VIDEO.mp4` (thumbnail opens the video for 1 s).
- Sample 12 frames from VIDEO.mp4 into a contact sheet and look at it before uploading.

## 9. Upload (Metricool, brand blogId `7850889`, YouTube channel UC9XemljFJXqS7VdjXSOcefg = Billion Dollar Mistakes; NOT UCy4RTiZ57S2HfvPEiRJ2Y3Q = personal channel)
1. Host the files on the throw-away branch `media` (one commit, force-pushed, so main never grows):
   ```
   cd /home/claude && rm -rf media && mkdir media && cp work/VIDEO.mp4 media/<date>-<slug>.mp4 && cp work/thumb.jpg media/<date>-<slug>.jpg
   cd media && git init -q -b media && git add . && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "media <date>" \
     && git push -f https://github.com/mees-byte/bom-media media
   ```
   Public URL: use the COMMIT-PINNED url `https://raw.githubusercontent.com/mees-byte/bom-media/<commit sha>/<file>` (the branch url is cached and 404s for minutes); check 200 with curl.
2. `createScheduledPost` with date `<slot>T17:00:00+01:00` (or +02:00 in summer time) and info JSON exactly like
   `examples/blockbuster/post_info.json`: autoPublish true, providers youtube, youtubeData {title (A), type video, privacy public,
   tags (≤ 490 chars total), category EDUCATION, madeForKids false, isAiGeneratedContent false}, videoThumbnailUrl,
   text = long SEO description (≥ 1,500 chars: hook sentences, "In this animated explainer…", What you'll learn, Sources, Chapters
   from the chapter scene times + 1 s, "Not financial advice. For education only.", credits, exactly 3 hashtags).
   If the thumbnail is rejected (VIDEO_THUMBNAIL_NOT_APPLICABLE), retry once without videoThumbnailUrl.
   The channel is phone-verified (2026-11-04), so custom thumbnails are allowed. If after publishing Metricool reports
   "Could not upload video thumbnail", set it with vidIQ `vidiq_update_video_thumbnail` on the new video ID and tell the owner.
3. Metricool copies the media to its own storage (the response shows static.metricool.com URLs). Nothing to clean up — the next run overwrites the `media` branch.

## 10. Shorts — 3 per long video, owner uploads them himself (owner choice 2026-11-05)
- Metricool free plan (20 posts/month) is reserved for the LONG videos. Do NOT schedule Shorts in Metricool anymore.
- For EVERY new long video cut **3 new Shorts** (20–30 s each) with `pipeline/shorts.py`, 0 credits:
  `python3 bom-media/pipeline/shorts.py work/VIDEO.mp4 <start> <dur> "<hook ≤ 6 words>" work/short_N.mp4`.
  Find exact start/end with caption strips (crop y 860–1060 of the long video, fps 2, tile) — word-position estimates run ~2–3 s early.
  Start on a sentence, end on a cliffhanger/question. Hook = short, punchy, true (number or twist), e.g. "BLOCKBUSTER ACTUALLY BEAT NETFLIX".
  Prefer: the twist, a big number, the "what does this mean for YOUR money" moment. Never reuse a segment already used as a Short.
- Write `work/upload/SHORTS - <topic>.txt` with per Short: title (#shorts), description ending with "Full story on the channel: <long title>",
  4 hashtags, 6 tags, related video = the long video, suggested times 09:00 / 13:00 / 21:00 NL on the day after the long video.
- **Upload (0 credits, no Metricool):** push the 3 mp4s to the `media` branch, then in the built-in browser (YouTube Studio, owner is signed in)
  open `studio.youtube.com/channel/UC9XemljFJXqS7VdjXSOcefg/videos/upload?d=ud`, inject the file with javascript_tool
  (fetch commit-pinned raw URL → File → DataTransfer → `ytcp-uploads-file-picker input[type=file]`, dispatch change).
  Set title/description with a real click on the field, then `execCommand('selectAll')` + `insertText` (plain typing right after upload garbles).
  "Not made for kids", tags via typing + Enter, then Plannen: date + time (click the time box, ctrl+a, type HH:MM, Enter). NEVER press Escape (closes the dialog).
  Related video needs a one-time channel verification the owner must do — skip until then.
- If the desktop app / browser is offline: send the 3 mp4s + the txt to the owner with SendUserFile (Dutch) so he uploads himself.

## 11. Finish
- Append to `pipeline/SCHEDULE.md` log: date, slot, title, topic, Metricool plannerUrl, credits used. Commit + push (never commit work/).
- **Message the owner (Dutch)**: `✅ Ingepland: "<titel>" — <dag datum> 17:00. Thumbnail + link: <plannerUrl>`.
- Any error you cannot fix: message the owner what failed and what you did instead. Never skip a slot silently.
