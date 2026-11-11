"""Update fields of a tracked row by Job URL: python3 update.py <csv> <job url> '<json fields>'"""
import csv, json, sys
if len(sys.argv) != 4:
    sys.exit(__doc__)
path, url, fields = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
with open(path, newline="", encoding="utf-8") as f:
    r = csv.DictReader(f); cols = r.fieldnames; rows = list(r)
hit = [x for x in rows if x["Job URL"] == url]
assert len(hit) == 1, f"{len(hit)} rows for {url}"
hit[0].update(fields)
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print("updated:", hit[0]["Company"], "|", hit[0]["Position"], "->", hit[0]["Status"])
