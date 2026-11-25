# Money Under Fire — "Social Security Retirement Checks Are Projected to Drop 22% in Late 2032 Unless Congress Acts" (Wed 2026-11-25)
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
exec(open(os.path.join(ROOT, "ckinds.py")).read())
KTEXT = {
    "countdown": "retirement oasi trust fund reserves 2026 2027 2028 2029 2030 2031 2032 october november december q4 2032 fourth quarter last three months reserves run out",
    "shrink": "average retirement check january 2027 $2,170 $1,693 78% $477 a month $5,700 a year today's dollars",
    "tank": "retirement trust fund reserves payroll tax in benefits out more in than out surplus saved more out than in drawn down q4 2032 fourth quarter",
    "grid78": "every $100 scheduled benefits $78 still paid $22 cut 78% 22% 100",
    "ages32": "who it would hit everyone on retirement benefits 60 66 70 76 age today",
    "shift": "retirement fund 2033 2032 last year's report this year one year closer",
    "reasons": "why long-term shortfall grew more than half lower expected birth rates about a third lower expected immigration about a quarter 2025 tax law income tax collected on benefits",
    "options": "close the gap 75 years congress acted today 34% payroll tax increase 25% cut all benefits 30% new beneficiaries only wait until 2034 40% tax increase 29% cut",
    "share": "know someone counting on every dollar send them this subscribe next report what changed in dollars",
    "bigcut": "22% retirees projected q4 2032 if congress does nothing now you know the number",
    "news": "trustees report june 9 2026 news fox business npr fortune newsweek aarp social security has less than 10 years before reserves are exhausted new trustees report warns funds could run short by 2032 program's trustees warn we are rapidly running out of time watchdog sounds alarm 22% cut confirmed for 2032 who could lose what in 2032 report projects trust fund shortfall in 2034",
    "law": "public law 98-21 social security amendments of 1983 signed april 20 1983 president reagan delayed june 1983 cost-of-living adjustment until december one-half of benefits taxable retirement age raised 67",
    "vote": "if it were your vote raise taxes cut benefits mix comment answer no politics",
    "y1983": "1983 early months away running dry march congress passed fix april president reagan signed yearly raise delayed six months income tax half benefits full retirement age 65 67",
}
exec(open(os.path.join(ROOT, "capskip.py")).read())
PR = "Quoted from SSA press release on the 2026 Trustees Report, June 9, 2026"

# --- cold open
sc("There is a date", "countdown", "navy", kicker="WRITTEN INTO SOCIAL SECURITY'S OWN REPORT", run=3.0, big="THE LAST 3 MONTHS OF 2032")
sc("On that date, unless", "doc", "navy", head="2026 TRUSTEES REPORT · SSA PRESS RELEASE",
   quote="The OASI Trust Fund reserves are projected to become depleted in the fourth quarter of 2032, with 78 percent of benefits payable at that time.",
   hl=["fourth quarter of 2032,", "78 percent"], dh=1.2, hs=3.0, cite=PR)
sc("For retirees, that's a", "bigcut", "navy", kicker="FOR RETIREES")
sc("Automatically.", "title", "navy", lines=[("AUTOMATICALLY.", CREAM), ("NO VOTE NEEDED.", GOLD)], size=130)
sc("On the average retirement", "hero", "navy", kicker="ON THE AVERAGE RETIREMENT CHECK", **{"from": 0, "to": 477}, label="LESS EVERY MONTH, IF THE CUT HITS IN Q4 2032", src="Illustration · today's dollars · SSA 2027 fact sheet · our math")
sc("It's a projection under", "title", "navy", kicker="IMPORTANT", lines=[("A PROJECTION UNDER CURRENT LAW", CREAM), ("NOT A FINAL DECISION", SOFT)], size=84)
sc("But it's the official", "title", "navy", lines=[("BUT IT'S", CREAM), ("THE OFFICIAL ONE.", GOLD)], size=130)
sc("This isn't a rumor,", "title", "navy", lines=[("NOT A RUMOR.", CREAM), ("NOT A POLITICIAN.", CREAM)], size=120)
sc("It's the 2026 Trustees", "news", "navy", title="HOW THE NEWS REPORTED THE 2026 TRUSTEES REPORT", gap=1.3, items=[
    dict(outlet="Fox Business", date="June 9, 2026", head="Social Security has less than 10 years before reserves are exhausted, new trustees report warns", y=330, dx=-150, rot=1.5, w=1250),
    dict(outlet="NPR (via OPB)", date="June 9, 2026", head="Social Security funds could run short by 2032, program's Trustees warn", y=545, dx=150, rot=-1.2, w=1250, hl=["by 2032,"]),
    dict(outlet="Fortune", date="June 9, 2026", head="'We are rapidly running out of time': Watchdog sounds Social Security alarm after 22% cut confirmed for 2032", y=772, dx=-60, rot=0.6, w=1400)], note="OUR NOTE: THE TRUSTEES PROJECT THIS UNDER CURRENT LAW. CONGRESS CAN STILL ACT.", dn=3.0)
sc("And this year, the", "shift", "navy")

# --- how a check shrinks
sc("So how does a", "title", "navy", lines=[("HOW DOES A CHECK", CREAM), ("JUST SHRINK?", GOLD)], size=130)
sc("Social Security's retirement benefits", "tank", "navy", phase=0)
sc("Now, more goes out", "tank", "navy", phase=1)
sc("And according to the", "tank", "navy", phase=2, drain=4.0)
sc("Here's the part people", "title", "navy", lines=[("RESERVES EMPTY", CREAM), ("≠ CHECKS STOP", GOLD)], size=150)
sc("Workers keep paying in.", "grid78", "navy", dc=2.0)
sc("78%. Not 100.", "title", "navy", lines=[("78%. NOT 100%.", CREAM), ("= THE 22% CUT", WARN)], size=140)
sc("Take the average retirement", "shrink", "navy", d=5.0)
sc("If Congress merged the", "note", "navy", kicker="IF CONGRESS MERGED RETIREMENT + DISABILITY FUNDS", big="2034 · ABOUT −17%", lines=["Still requires a vote", "Per CRFB · Trustees: combined funds 83% payable"], src="CRFB analysis · SSA press release", col=STEELC)
sc("the date would be", "news", "navy", title="THE 2034 VIEW (COMBINED FUNDS)", items=[dict(outlet="AARP", date="on the 2026 report", head="Social Security Report Projects Trust Fund Shortfall in 2034", y=470, hl=["2034"])])
sc("And the Committee for", "note", "navy", kicker="CRFB ESTIMATE (EARLIER WORK, SIMILAR CUT)", big="−$18,400 A YEAR", lines=["Typical couple retiring in 2033", "Both spouses combined"], src="Committee for a Responsible Federal Budget", col=(120, 54, 30), bcol=WARN)
sc("Now, who would that", "news", "navy", title="IN THE NEWS", items=[dict(outlet="Newsweek", date="Nov 9, 2026", head="Social Security cut: Who could lose what in 2032?", y=470, hl=["Who could lose what"])])
sc("If you're 60 today,", "ages32", "navy")

# --- why it got worse
sc("So why did things", "title", "navy", lines=[("WHY DID IT", CREAM), ("GET WORSE?", GOLD)], size=150)
sc("For the retirement fund,", "shift", "navy")
sc("And the long-term shortfall", "reasons", "navy", d=[4.8, 8.5, 11.5])
sc("Fewer future workers paying", "title", "navy", lines=[("FEWER PAYING IN.", CREAM), ("LESS FLOWING BACK.", CREAM), ("SAME PROMISES.", GOLD)], size=110)

# --- the fix
sc("And here's the most", "title", "navy", kicker="THE MOST CONTROVERSIAL PART", lines=[("SOMEONE HAS TO PAY", GOLD)], size=130)
sc("The Budget Committee ran", "options", "navy", d=[6.0, 9.3, 12.0])
sc("And the longer they", "options", "navy", title="IF CONGRESS WAITS UNTIL 2034", opts=[("+40%", "PAYROLL TAX", "+4.9 points", STEELC), ("−29%", "ALL BENEFITS", "everyone", (120, 54, 30))], d=[4.2, 6.2])
sc("So here's my question,", "vote", "navy")

# --- 1983
sc("Now, has this happened", "title", "navy", lines=[("HAS THIS", CREAM), ("HAPPENED BEFORE?", GOLD)], size=140)
sc("In the early 1980s,", "y1983", "navy", run=9.0)
sc("When Congress finally passed", "doc", "navy", head="CONGRESSIONAL RESEARCH SERVICE · REPORT R47040",
   quote="When the 1983 amendments were passed, Social Security was months or weeks away from being unable to pay full benefits.",
   hl=["months or weeks away"], dh=1.5, hs=1.5, cite="Quoted from CRS report R47040 (March 4, 2022)")
sc("President Reagan signed it", "law", "navy", ds=0.6, drows=[6.2, 6.5, 8.3, 8.6, 12.2], rows=[
    ("\"Delayed the June 1983 cost-of-living adjustment", True), ("  until December 1983\"", True), ("Up to \"one-half of Social Security benefits\"", True), ("  taxable, above certain incomes", True), ("Retirement age raised \"in two stages to 67\"", True)])
sc("That's why your full", "title", "navy", kicker="BORN IN 1960 OR LATER?", lines=[("FULL RETIREMENT AGE: 67", GOLD), ("THE LAST BIG FIX", CREAM)], size=110)
sc("So, the question was", "title", "navy", lines=[("NOT WHETHER CONGRESS ACTS.", CREAM), ("WHO PAYS.", GOLD)], size=130)

# --- close
sc("If you know someone", "share", "navy")
sc("This is general education,", "title", "navy", lines=[("GENERAL EDUCATION", CREAM), ("A PROJECTION, NOT A DECISION", SOFT)], size=90)
sc("So, back to that", "countdown", "navy", kicker="RETIREMENT FUND, IF CONGRESS DOES NOTHING", run=1.2, big="LAST 3 MONTHS OF 2032", sub="ABOUT 6 YEARS FROM NOW")
sc("22%. And now, you", "bigcut", "navy", kicker="NOW YOU KNOW THE NUMBER")
