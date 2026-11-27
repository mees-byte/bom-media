# Money Under Fire — "Medicare Part D 2027: Premiums Could Jump 50% Unless You Switch by December 7" (Fri 2026-11-27)
# Intro rules (STYLE 2026-11-27): answer the thumbnail in 10 s, open one bigger loop, no roadmap, disclaimers short.
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
exec(open(os.path.join(ROOT, "ckinds.py")).read())
exec(open(os.path.join(ROOT, "pkinds.py")).read())
KTEXT = {
    "tag": "average stand-alone drug plan premium if you keep your plan per month $34 $51 50% 2026 2027 thirty-four fifty-one",
    "deadline": "december 2026 7 7th open enrollment ends december 7",
    "twonums": "two real analyses two different questions kff 50% $34 $51 if people keep their plan medicare cms less than $1 $35.09 $36 national average",
    "people": "13.6 million people stand-alone plans no extra help 76% pay more if they change nothing",
    "range": "8 national drug plans average monthly premium 2027 $6.50 cheapest $204.50 priciest cheapest premium cheapest plan drugs",
    "fork": "by december 7 compare plans medicare plan finder ship keep your plan continues 2027 price knowing what it will cost",
    "news": "kff average monthly premium medicare part d stand-alone plans projected increase 50% $34 $51 2027 unless enrollees switch lower-cost plans",
}
exec(open(os.path.join(ROOT, "capskip.py")).read())
KTEXT["fork"] = KTEXT["fork"]
PX = lambda n: f"px:{n}"; PXB = lambda n: f"pxb:{n}"

# 0:00 — the thumbnail's answer, immediately
sc("50%.", "photo", PXB("woman_face"), lines=[("+50%", WARN), ("AVG STAND-ALONE DRUG PLAN PREMIUM, 2027 · IF PEOPLE KEEP THEIR PLAN", CREAM)], size=200, y=800)
sc("From $34 a", "tag", "navy", d=0.3, sub="IF PEOPLE KEEP THE PLAN THEY HAVE", ds=3.0)
sc("And the open enrollment", "deadline", "navy")
sc("But here's the strange", "title", PX("woman_wide"), lines=[("BUT MEDICARE SAYS…", CREAM)], size=120)
sc("Medicare itself says the", "twonums", "navy", d=[0.2, 0.3], dv=2.0)
sc("And what you actually", "title", "navy", kicker="WHAT YOU PAY IN 2027", lines=[("MAY DEPEND ON A CHOICE", CREAM), ("BY DECEMBER 7", GOLD)], size=110)

# KFF
sc("Let's start with the", "news", "navy", title="THE 50% NUMBER", items=[dict(outlet="KFF", date="Oct 30, 2026",
   head="The Average Monthly Premium for Medicare Part D Stand-Alone Plans Is Projected to Increase by 50% From $34 to $51 in 2027 Unless Enrollees Switch to Lower-Cost Plans", y=520, w=1500, hl=["Unless Enrollees Switch"])])
sc("They looked at standalone", "title", "navy", kicker="KFF LOOKED AT", lines=[("STAND-ALONE DRUG PLANS", CREAM), ("ADDED TO ORIGINAL MEDICARE", GOLD)], size=96)
sc("If everyone stays in", "tag", "navy", d=2.6)
sc("That's about $17 more", "note", "navy", kicker="ON AVERAGE, STAND-ALONE PLANS, IF YOU KEEP YOURS", big="+$17/MO ≈ $200/YR", lines=["Much more for some, less for others"], src="KFF · our math", col=(120, 54, 30), bcol=WARN)
sc("If you have a", "note", "navy", kicker="HAVE MEDICARE ADVANTAGE WITH DRUGS? THE +50% ISN'T YOUR NUMBER", big="≈ $9/MO", lines=["Avg Medicare Advantage drug premium, 2027"], src="KFF, Oct 30, 2026", col=TEAL, bcol=(120, 220, 160))

# CMS
sc("Now Medicare's number.", "doc", "navy", head="CMS PRESS RELEASE · SEPT 28, 2026",
   quote="Stand-alone drug plan premium \"projected to increase less than $1, from $35.09 in 2026 to $36 in 2027.\"",
   hl=["less than $1,"], dh=2.0, hs=1.5, cite="Quoted from CMS press release, September 28, 2026")
sc("So which is it?", "twonums", "navy", d=[0.0, 0.0], dv=0.0)
sc("KFF's number answers one", "title", "navy", kicker="KFF'S QUESTION", lines=[("WHAT HAPPENS TO PEOPLE", CREAM), ("WHO DON'T SWITCH?", GOLD)], size=110)

# why
sc("Why are prices jumping?", "title", PX("woman_wide"), lines=[("WHY ARE PREMIUMS", CREAM), ("JUMPING?", GOLD)], size=150)
sc("Since 2025, Medicare has", "note", "navy", kicker="PART D PREMIUM STABILIZATION DEMONSTRATION", big="2025 – 2026", lines=["Extra money to plans + a cap on premium increases", "2026 cap: $50 a month"], src="KFF · CMS", col=STEELC, bcol=CREAM)
sc("After 2026, the program", "title", "navy", lines=[("AFTER 2026:", CREAM), ("THE PROGRAM ENDS", WARN)], size=140)

# who
sc("Here's who feels it.", "people", "navy", dc=9.0, n=76)
sc("More than 4 million", "note", "navy", kicker="4+ MILLION IN $0-PREMIUM STAND-ALONE PLANS TODAY", big="2027: NO $0 STAND-ALONE PLANS", lines=["No zero-premium stand-alone plans next year"], src="KFF, Oct 30, 2026", col=(120, 54, 30), bcol=WARN)
sc("And about 2.4 million", "note", "navy", kicker="IF THEY STAY IN THE SAME PLAN", big="2.4 MILLION", lines=["Premium up more than $50 a month"], src="KFF analysis, Oct 30, 2026", col=(120, 54, 30), bcol=WARN)
sc("Among the eight national", "range", "navy")
sc("So here's my question.", "title", "navy", kicker="TELL ME IN THE COMMENTS ↓", lines=[("CHECKED YOUR 2027 PRICE?", CREAM), ("OR LETTING IT ROLL OVER?", GOLD)], size=100)

# other numbers
sc("Two more numbers changed.", "options", "navy", title="TWO MORE 2027 PART D NUMBERS", srcl="KFF · CURE (Nov 11, 2026)",
   opts=[("$700", "DEDUCTIBLE", "standard · was $615", STEELC), ("$2,400", "OUT-OF-POCKET CAP", "excl. premiums · was $2,100", (120, 54, 30))], d=[4.8, 10.6], noor=True)

# do nothing
sc("So what happens if", "title", "navy", lines=[("WHAT IF YOU", CREAM), ("DO NOTHING?", GOLD)], size=150)
sc("Medicare says people who", "doc", "navy", head="CMS PRESS RELEASE · SEPT 28, 2026",
   quote="People who want to keep their current Medicare coverage generally do not need to re-enroll.",
   hl=["generally do not need to re-enroll."], dh=1.0, hs=1.5, cite="CMS press release, Sep 28, 2026 · In most cases your plan continues with its 2027 premium, drug list and costs")
sc("If your plan is", "title", "navy", kicker="PLAN CHANGING OR LEAVING YOUR AREA?", lines=[("WATCH FOR A NOTICE", GOLD)], size=120)
sc("So you can compare", "fork", "navy")
sc("If you want unbiased", "note", "navy", kicker="WANT HELP COMPARING?", big="SHIP COUNSELORS", lines=["Unbiased, one-on-one help", "shiphelp.org"], src="shiphelp.org", col=TEAL, bcol=CREAM)
sc("This is general education,", "title", "navy", lines=[("GENERAL EDUCATION", CREAM), ("NOT PERSONAL ADVICE", SOFT)], size=100)
sc("If someone you love", "title", PX("woman_face"), kicker="KNOW SOMEONE ON A DRUG PLAN?", lines=[("SHARE THIS WITH THEM", GOLD)], size=110)
sc("So 50% or less", "twonums", "navy", d=[0.0, 0.0], dv=0.0)
sc("For many people in", "deadline", "navy", sub="FOR MANY IN STAND-ALONE PLANS: IT DEPENDS ON WHAT YOU DO BY DEC 7", srcl="Open enrollment ends Dec 7 · CMS")
