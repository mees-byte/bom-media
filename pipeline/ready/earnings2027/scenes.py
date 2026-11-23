# Money Under Fire — "Her Social Security Checks Stopped Coming. She Did Nothing Wrong." (2027 earnings test, story format)
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
exec(open(os.path.join(ROOT, "ekinds.py")).read())
PXB = lambda n, fb="navy": (f"pxb:{n}" if os.path.exists(os.path.join(ROOT, "px", n + ".jpg")) else fb)
PX = lambda n, fb="navy": (f"px:{n}" if os.path.exists(os.path.join(ROOT, "px", n + ".jpg")) else fb)
SSP = ("Feb 3", "SOCIAL SECURITY", "NOT RECEIVED", WARN, 0.9)
PAY = lambda d_: (d_, "PAYCHECK", "+$1,136", (30, 140, 90), 0.5)

# --- cold open: the empty deposits
sc("It's February twenty", "bankapp", PX("kitchen_phone"), fic=True, lines=["FEBRUARY 2027", ("LINDA, 63", GOLD)],
   rows=[("Jan 3", "SOCIAL SECURITY", "+$1,400.00", (30, 140, 90), 0.4), PAY("Jan 30"), ("Feb 3", "SOCIAL SECURITY", "— — —", WARN, 1.2)])
sc("Nothing. No fourteen", "bankapp", PX("kitchen_phone"), fic=True, lines=[("NO $1,400", WARN), "JUST HER PAYCHECK"],
   rows=[PAY("Jan 30"), ("Feb 3", "SOCIAL SECURITY", "NOT RECEIVED", WARN, 0.3), PAY("Feb 13")], stamp=("MISSING", 1.0))
sc("March. Nothing again.", "bankapp", PX("calendar"), fic=True, lines=["MARCH. APRIL.", ("MAY.", GOLD)],
   rows=[("Mar 3", "SOCIAL SECURITY", "NOT RECEIVED", WARN, 0.1), ("Apr 3", "SOCIAL SECURITY", "NOT RECEIVED", WARN, 0.6), ("May 3", "SOCIAL SECURITY", "NOT RECEIVED", WARN, 1.1)])
sc("Linda isn't a real", "title", "navy", kicker="LINDA IS MADE UP", lines=[("HER NUMBERS AREN'T", CREAM), ("REAL 2027 RULES", GOLD)], size=110)
sc("Because her checks weren't", "title", PX("folder"), lines=[("NOT LOST.", CREAM), ("HELD.", GOLD)], size=170)
sc("Her three point six", "linkvid", "navy", label="HER 3.6% RAISE: NOT A CENT FOR 4 MONTHS")

# --- last fall
sc("So let's go back", "title", PXB("autumn_street"), kicker="LAST FALL", lines=[("HOW IT STARTED", CREAM)], size=120)
sc("Linda claimed Social Security", "hero", PX("retiree_desk"), kicker="LINDA CLAIMED AT 63", **{"from": 0, "to": 1400}, label="A MONTH FROM SOCIAL SECURITY", src="Illustrative example")
sc("Then a hardware store", "photo", PXB("hardware_store"), lines=[("~30 HOURS A WEEK", CREAM), ("$35,560 A YEAR", GOLD)], y=760)
sc("When Social Security asked", "title", PX("paperwork"), kicker="SHE TOLD SOCIAL SECURITY", lines=[("\"I'LL EARN $35,560\"", CREAM)], size=110)
sc("What she didn't realize", "title", "navy", lines=[("WHAT THAT ANSWER", CREAM), ("SET IN MOTION", GOLD)], size=110)

# --- the number
sc("Here's the number.", "hero", PXB("cash_counter"), kicker="THE 2027 EARNINGS LIMIT", **{"from": 0, "to": 25560}, label="IF YOU CLAIM BEFORE FULL RETIREMENT AGE", src="Source: SSA 2027 COLA fact sheet")
sc("That's the twenty twenty-seven limit", "ages", "navy", d=[0.2, 99, 99])
sc("Earn more than that", "dollar", "navy")
sc("So every extra dollar", "dollar", "navy")
sc("She was ten thousand", "limitbar", "navy", earn=35560, half=True, fic=True)
sc("Now, you'd expect them", "title", "navy", lines=[("A LITTLE FROM EACH CHECK?", CREAM), ("NO.", WARN)], size=110)
sc("Social Security stops WHOLE", "held", "navy")
sc("So they held four.", "year", "navy", held=4, dh=0.3, fic=True, foot="4 × $1,400 = $5,600 HELD")
sc("The extra six hundred", "year", "navy", held=4, dh=0, fic=True, foot="CHECK FOR MAY → LANDS IN JUNE · FULL FROM THEN ON", df=1.2)

# --- Harold
sc("Now meet her neighbor,", "vs", PX("suburb_houses"), d2=0.2, dr=99)
sc("Harold doesn't work.", "title", PX("investments"), kicker="HAROLD (ALSO MADE UP)", lines=[("PENSION · ANNUITY", CREAM), ("INTEREST · DIVIDENDS · GAINS", GOLD)], size=90)
sc("Harold's checks weren't touched.", "vs", PX("suburb_houses"), d2=0, dr=0.3)
sc("Because the limit only", "counts", "navy", dno=3.2, gap=0.35)
sc("So which one would", "choice", "navy", q="WOULD YOU HAVE TAKEN THE JOB?", sides=["Works, checks held", "Doesn't work"])

# --- the turn
sc("Here's where Linda's story", "title", PX("phone_call"), kicker="SHE CALLED SOCIAL SECURITY", lines=[("\"THE MONEY ISN'T LOST\"", GOLD)], size=110)
sc("When Linda reaches full", "title", "navy", kicker="AT FULL RETIREMENT AGE", lines=[("BENEFIT RECALCULATED", CREAM), ("CREDIT FOR HELD MONTHS", GOLD)], size=100)
sc("So that's the good", "title", "navy", lines=[("THE PART THE CALL", CREAM), ("SKIPPED", WARN)], size=130)
sc("Social Security's own booklet", "payback", "navy", fill=6.0)
sc("So yes, it comes", "photo", PXB("hourglass"), lines=[("IT COMES BACK.", CREAM), ("SLOWLY.", GOLD)], y=760)
sc("One exception: spouses", "title", "navy", kicker="EXCEPTION", lines=[("SPOUSES & SURVIVORS CARING", CREAM), ("FOR A YOUNG/DISABLED CHILD", CREAM), ("NO INCREASE", WARN)], size=74)

# --- timing
sc("Now, what if Linda's", "title", PXB("clock"), lines=[("WHAT IF HER TIMING", CREAM), ("WAS DIFFERENT?", GOLD)], size=110)
sc("There's a second limit,", "ages", "navy", d=[0.0, 0.3, 99])
sc("And from that month", "ages", "navy", d=[0.0, 0.0, 0.3])
sc("And if Linda had", "firstyear", "navy")

# --- close
sc("If someone you know", "share", "navy")
sc("This is general education,", "title", "navy", lines=[("GENERAL EDUCATION", CREAM), ("NOT FINANCIAL ADVICE", SOFT)], size=90)
sc("So, back to February.", "bankapp", PX("kitchen_phone"), fic=True, lines=["NOTHING WENT WRONG.", ("THE RULE WORKED.", GOLD)],
   rows=[("Feb 3", "SOCIAL SECURITY", "HELD", WARN, 0.2), ("Jun 3", "SOCIAL SECURITY", "+$1,400.00", (30, 140, 90), 0.8)])
sc("You don't have to.", "hero", "navy", kicker="NOW YOU KNOW THE NUMBER", **{"from": 0, "to": 25560}, label="BEFORE IT KNOWS YOU", src="SSA 2027 COLA fact sheet")
