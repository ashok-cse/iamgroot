"""Append one application row to the tracker: python3 track.py <csv> '<json object>'"""
import csv, json, sys
COLS = ["Company","Position","Location","Country","Job URL","Application URL","Date Applied","Application Method","Recruiter/HR Contact","Email Address","Salary Info","Start Date Info","Visa Sponsorship Info","Status","Notes","Custom Message Sent"]
row = json.loads(sys.argv[2])
unknown = set(row) - set(COLS)
assert not unknown, unknown
with open(sys.argv[1], newline="", encoding="utf-8") as f:
    existing = list(csv.DictReader(f))
dup = [r for r in existing if r["Job URL"] == row.get("Job URL")]
if dup:
    sys.exit("DUPLICATE: already tracked " + row.get("Job URL", ""))
with open(sys.argv[1], "a", newline="", encoding="utf-8") as f:
    csv.DictWriter(f, fieldnames=COLS).writerow({c: row.get(c, "") for c in COLS})
print(f"tracked #{len(existing)+1}: {row.get('Company')} | {row.get('Position')}")
