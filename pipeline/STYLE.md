# STYLE — lessons (apply to every video)

- 2026-11-03: Voice = Arthur (C1npRmjB19a6yNkEucvx) on eleven_v4 with delivery tags. Owner found multilingual_v2 too slow; v4 + tags = faster, more conviction.
- 2026-11-03: 480–520 words ≈ 3:15–3:30 with v4. 536 words gave 3:28.
- 2026-11-03: Real company logos on white plates instead of brand names as text (owner request).
- 2026-11-03: Every scene starts with a short zoom punch + slow push-in; impact sound on big numbers.
- 2026-11-04: NO whoosh/sweep sound on scene changes or chapters (owner found it annoying). Removed from mix.py.
- 2026-11-03: Never use invented chart data; without real numbers use a text animation.
- 2026-11-03: Keep on-screen content above y≈900 so it never collides with the captions.
- 2026-11-04: Wikimedia rate-limits (429) after ~4 quick downloads, for a long time. Download ALL logos first, one per ~10 s, before anything else; use direct md5 upload paths, not the API search.
- 2026-11-04: Force-pushing the `media` branch is blocked in automated runs. Instead: `git fetch origin media`, worktree on origin/media, `git rm` old files, add new ones, normal commit + push. raw URLs still work.
- 2026-11-04: mix.py chdirs into VIDEO_DIR — pass ABSOLUTE paths for thumb and music.
- 2026-11-04: count kind with logo + kicker used to overlap the number; fixed in render.py (number moved down). Check one count frame anyway.
- 2026-11-04: Don't put quote marks around a company promise unless the exact words are sourced.
- 2026-11-04: Don't transcribe the music to check for vocals (costs ~1.2k credits); the "Instrumental only, no vocals" prompt was reliable.
- 2026-11-04: vidIQ credits are limited (150/month). Max 1 vidIQ call per trend run, none in evergreen runs; weekly review max 2 calls. Use WebSearch + Metricool analytics first.
- 2026-11-04: Thumbnails = same design as the video (pipeline/thumb.py): company logo on white plate, WHITE text, question marks. Owner disliked the AI-generated vault thumbnails. Owner picked the dark "WHO STOLE $6.3 BILLION?" layout over a red one.
- 2026-11-04: Owner wants better visuals: mix 4–6 Pixabay stock clips (b-roll kind) between the animations. Mood shots only, no people, never as fake evidence.
