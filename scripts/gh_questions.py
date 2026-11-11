"""Print Greenhouse application questions: python3 gh_q.py <board> <job_id> [<board> <job_id> ...]"""
import json, sys, urllib.request, re, html
def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (job-board-reader)"})
    with urllib.request.urlopen(req, timeout=20) as r: return json.loads(r.read().decode())
args = sys.argv[1:]
for board, jid in zip(args[0::2], args[1::2]):
    try:
        d = get(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{jid}?questions=true")
    except Exception as e:
        print(f"=== {board}/{jid}: ERROR {e}\n"); continue
    print(f"=== {board}/{jid} | {d.get('title')} | {(d.get('location') or {}).get('name')}")
    print("URL:", d.get("absolute_url"))
    for group in ("questions", "location_questions", "compliance", "demographic_questions"):
        qs = d.get(group) or []
        if isinstance(qs, dict): qs = qs.get("questions", [])
        for q in qs:
            label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(q.get("label") or q.get("description") or ""))).strip()
            for f in q.get("fields", []) or [{}]:
                vals = [v.get("label") for v in (f.get("values") or [])]
                print(f"  [{group[:4]}] {'*' if q.get('required') else ' '} {label[:150]} <{f.get('name')}:{f.get('type')}>" + (f" opts={vals[:12]}" if vals else ""))
    print()
