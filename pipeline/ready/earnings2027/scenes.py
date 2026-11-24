# Money Under Fire — "Her Social Security Checks Stopped Coming. She Did Nothing Wrong." (2027 earnings test, story format)
# anchors = transcript words (align.py + clean.py: numbers as digits)
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
exec(open(os.path.join(ROOT, "ekinds.py")).read())
PXB = lambda n, fb="navy": (f"pxb:{n}" if os.path.exists(os.path.join(ROOT, "px", n + ".jpg")) else fb)
PX = lambda n, fb="navy": (f"px:{n}" if os.path.exists(os.path.join(ROOT, "px", n + ".jpg")) else fb)
PAY = lambda d_, dl=0.5: (d_, "PAYCHECK", "+$1,136", (30, 140, 90), dl)
NR = lambda d_, dl: (d_, "SOCIAL SECURITY", "NOT RECEIVED", WARN, dl)

# --- cold open: the empty deposits
sc("It's February", "bankapp", PX("linda_face"), fic=True, lines=["FEBRUARY 2027", ("LINDA, 63", GOLD)],
   rows=[("Jan 20", "SOCIAL SECURITY", "+$1,400.00", (30, 140, 90), 0.4), PAY("Jan 29", 0.7)])
sc("She checks her bank", "bankapp", PX("linda_table"), fic=True, lines=["PAYDAY FOR", ("SOCIAL SECURITY", GOLD)],
   rows=[("Jan 20", "SOCIAL SECURITY", "+$1,400.00", (30, 140, 90), 0.0), PAY("Jan 29", 0.0), ("Feb 17", "SOCIAL SECURITY", "— — —", WARN, 1.2)])
sc("No $1,400", "bankapp", PX("linda_table"), fic=True, lines=[("NO $1,400", WARN), "JUST HER PAYCHECK"],
   rows=[PAY("Feb 12", 0.0), NR("Feb 17", 0.2), PAY("Feb 26", 0.5)], stamp=("MISSING", 0.8))
sc("March. Nothing again.", "bankapp", PX("linda_face"), fic=True, lines=["MARCH. APRIL.", ("MAY.", GOLD)],
   rows=[NR("Mar 17", 0.1), NR("Apr 21", 1.0), NR("May 19", 1.9)])
sc("Linda isn't a real", "photo", PXB("linda_wide"), lines=[("LINDA IS MADE UP", CREAM), ("THE 2027 RULES ARE REAL", GOLD)], y=800)
sc("And if you're claiming", "title", "navy", kicker="IF YOU'RE CLAIMING AND STILL WORKING", lines=[("THIS CAN HAPPEN", CREAM), ("TO YOU", GOLD)], size=120)
sc("Because her checks weren't", "title", PX("linda_face"), lines=[("NOT LOST.", CREAM), ("HELD.", GOLD)], size=170)
sc("On purpose.", "title", "navy", lines=[("ON PURPOSE.", CREAM)], size=150)
sc("And the reason is", "title", "navy", lines=[("ONE NUMBER", GOLD), ("SHE'D NEVER HEARD OF", CREAM)], size=110)
sc("Her 3.6% raise", "linkvid", "navy", label="HER 3.6% RAISE: NOT A CENT FOR 4 MONTHS")

# --- last fall
sc("So, let's go back", "title", PXB("linda_wide"), kicker="LAST FALL", lines=[("HOW IT STARTED", CREAM)], size=120)
sc("Linda claims Social Security", "hero", PX("linda_face"), kicker="LINDA CLAIMED AT 63", **{"from": 0, "to": 1400}, label="A MONTH FROM SOCIAL SECURITY", src="Illustrative example")
sc("Then, a hardware store", "title", "navy", kicker="A PART-TIME JOB", lines=[("~30 HOURS A WEEK", CREAM)], size=120)
sc("Good people. Steady pay.", "hero", "navy", kicker="WHAT SHE'LL EARN IN 2027", **{"from": 0, "to": 35560}, label="FROM HER PART-TIME JOB", src="Illustrative example")
sc("When Social Security asked", "title", PX("linda_table"), kicker="SHE TOLD SOCIAL SECURITY", lines=[("\"I'LL EARN $35,560\"", CREAM)], size=110)
sc("What she didn't realize", "title", "navy", lines=[("WHAT THAT ANSWER", CREAM), ("SET IN MOTION", GOLD)], size=110)

# --- the number
sc("Here's the number.", "hero", "navy", kicker="THE 2027 EARNINGS LIMIT", **{"from": 0, "to": 25560}, label="IF YOU CLAIM BEFORE FULL RETIREMENT AGE", src="Source: SSA 2027 COLA fact sheet")
sc("That's the 2027 limit", "ages", "navy", d=[0.2, 99, 99])
sc("Earn more than that", "dollar", "navy", nocap=True)
sc("So, every extra dollar", "dollar", "navy")
sc("She was $10,000 over.", "limitbar", "navy", earn=35560, half=True, fic=True)
sc("Now, you'd expect them", "title", "navy", lines=[("A LITTLE FROM EACH CHECK?", CREAM)], size=110)
sc("They don't.", "title", "navy", lines=[("NO.", WARN)], size=220)
sc("Social Security stops whole", "held", "navy", d0=4.6)
sc("So, they held four.", "year", "navy", held=4, dh=0.3, fic=True, foot="4 × $1,400 = $5,600 HELD", df=2.0)
sc("The extra $600 they", "year", "navy", held=4, dh=0, fic=True, foot="EXTRA $600 → PAID BACK THE NEXT YEAR", df=0.4)
sc("And starting with her", "year", "navy", held=4, dh=0, fic=True, foot="CHECK FOR MAY → LANDS IN JUNE · FULL FROM THEN ON", df=0.6)

# --- Harold
sc("Now meet her neighbor,", "photo", PXB("harold_wide"), lines=[("HAROLD, 63", CREAM), ("ALSO MADE UP", SOFT)], y=800)
sc("Also 63. Also claimed", "vs", "navy", d2=0.2, dr=99)
sc("Harold doesn't work.", "title", PX("harold_face"), kicker="HAROLD DOESN'T WORK", lines=[("PENSION · ANNUITY", CREAM), ("INTEREST · DIVIDENDS · GAINS", GOLD)], size=90)
sc("Harold's checks weren't touched.", "vs", "navy", d2=0, dr=0.3)
sc("Because the limit only", "title", "navy", kicker="THE LIMIT ONLY COUNTS", lines=[("MONEY YOU EARN", CREAM), ("FROM WORK", GOLD)], size=120)
sc("Wages, bonuses, commissions,", "counts", "navy", dno=5.4, gap=0.5)
sc("So, which one would", "choice", "navy", q="WOULD YOU HAVE TAKEN THE JOB?", sides=["Works, checks held", "Doesn't work"])

# --- the turn
sc("Here's where Linda's story", "title", PX("linda_table"), kicker="SHE CALLED SOCIAL SECURITY", lines=[("ANGRY.", WARN)], size=150)
sc("And the person on", "title", PX("linda_face"), kicker="SSA'S OWN BOOKLET", lines=[("\"THE MONEY ISN'T LOST\"", GOLD)], size=110)
sc("When Linda reaches full", "title", "navy", kicker="AT FULL RETIREMENT AGE", lines=[("BENEFIT RECALCULATED", CREAM), ("CREDIT FOR HELD MONTHS", GOLD)], size=100)
sc("Her monthly check goes", "title", "navy", lines=[("HIGHER CHECK", GOLD), ("FOR LIFE", CREAM)], size=130)
sc("So that's the good", "title", "navy", lines=[("THE PART THE CALL", CREAM), ("SKIPPED", WARN)], size=130)
sc("Social Security's own booklet runs", "payback", "navy", fs=13.0, fill=8.8)
sc("So yes, it comes", "photo", PXB("linda_wide"), lines=[("IT COMES BACK.", CREAM), ("SLOWLY.", GOLD)], y=800)
sc("And the longer you", "title", "navy", lines=[("LIVE LONGER =", CREAM), ("GET MORE BACK", GOLD)], size=120)
sc("One exception.", "title", "navy", kicker="ONE EXCEPTION", lines=[("SPOUSES & SURVIVORS CARING", CREAM), ("FOR A YOUNG/DISABLED CHILD", CREAM), ("NO INCREASE", WARN)], size=74)

# --- timing
sc("Now, what if Linda's", "title", "navy", lines=[("WHAT IF HER TIMING", CREAM), ("WAS DIFFERENT?", GOLD)], size=110)
sc("There's a second limit.", "ages", "navy", d=[0.0, 0.3, 99])
sc("And from that month", "ages", "navy", d=[0.0, 0.0, 0.3])
sc("You can earn a", "title", "navy", kicker="FROM FULL RETIREMENT AGE", lines=[("EARN $1,000,000", CREAM), ("$0 HELD BACK", GOLD)], size=120)
sc("And if Linda had", "firstyear", "navy", dt=12.2)

# --- close
sc("If someone you know", "share", "navy")
sc("This is general education,", "title", "navy", lines=[("GENERAL EDUCATION", CREAM), ("NOT FINANCIAL ADVICE", SOFT)], size=90)
sc("So, back to February.", "bankapp", PX("linda_face"), fic=True, lines=["NOTHING WENT WRONG.", ("THE RULE WORKED.", GOLD)],
   rows=[("Feb 17", "SOCIAL SECURITY", "HELD", WARN, 0.2), ("Jun 16", "SOCIAL SECURITY", "+$1,400.00", (30, 140, 90), 0.8)])
sc("She just met it", "photo", PXB("linda_wide"), lines=[("SHE MET THE RULE", CREAM), ("WITH HER OWN MONEY", GOLD)], y=800)
sc("You don't have to.", "hero", "navy", kicker="NOW YOU KNOW THE NUMBER", **{"from": 0, "to": 25560}, label="BEFORE IT KNOWS YOU", src="SSA 2027 COLA fact sheet")

label_fiction(S)
