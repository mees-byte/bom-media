# READY: "It's official: 2027 Medicare Part B premium" (prepared 2026-11-17, fact check PASS on projections)

Why this topic (channel data 1–17 Nov): the COLA video (iDK0PUrk6L0) is the only real performer — 91 engaged views,
the only video with suggested-video traffic (14 views, 56% retention). This is its direct sequel: the COLA video said
the official Part B number "comes later in November". Same lane: a concrete dollar amount on the viewer's own check.

## Announcement-day checklist (CMS fact sheet "2027 Medicare Parts A & B Premiums and Deductibles")
1. Put the official premium, increase, deductible into values.json (num + spoken). NET = 75 − increase (round), HH = increase / 0.036.
2. Replace the 2026 IRMAA numbers in the template (Group two) with the 2027 thresholds + first-tier total if CMS published them;
   keep "For twenty twenty-six…" wording only if not.
3. If the video goes out after Dec 7: delete the "you still have until December seventh" line.
4. If the official increase is LARGER than the COLA dollars for typical benefits, rewrite the "good news" lines — don't publish the template blind.
5. `python3 fill.py <dir>` → NARRATION.txt, quick re-check of the changed lines (Agent), then voice (Arthur v4, atempo 1.08).
6. Publish the SAME day (search peak). Pin comment, add to the COLA playlist, end screen → COLA video.

## Titles (plain words, keyword up front)
A. Medicare Part B 2027 Is Official: Here's What's Left of Your $75 Raise   ← pick
B. It's Official: Your 2027 Medicare Premium Is {{PREMIUM}}. Here's What You'll Actually Get
C. 2027 Medicare Premium Announced: Who Pays More (and Who Pays Nothing)

## Thumbnail (same style as the $75 video — owner's AI photo + our overlay)
Text: "$75 RAISE?" (white) + "{{NET}} LEFT" (gold) — or "IT'S OFFICIAL" + "{{PREMIUM}}".

## Chapters
0:00 The answer · Ch1 The math · Ch2 Why most people are protected · Ch3 Who gets a different number · Ch4 The program most people skip · Ch5 What to check this week

## Pinned comment
Is this year's raise going to cover your rising costs — or not even close? And did you know about Medicare Savings Programs?

## Shorts (3)
1. "$75 RAISE, {{NET}} LEFT" — hook
2. "YOUR 2025 TAXES SET THIS BILL" — IRMAA 2-year lookback
3. "THE STATE CAN PAY YOUR PREMIUM" — Medicare Savings Programs (no "%" in hooks)
