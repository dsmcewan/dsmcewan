#!/usr/bin/env python3
"""Verify the article index and quoted claims against the live Anthropic pages.

Usage:
  python3 verify_live.py --source live      # fetch https://www.anthropic.com/engineering/<slug>
  python3 verify_live.py --source mirror    # fetch the public archive (for environments that cannot reach anthropic.com)

For every article in IMPLEMENTATION_PLAN.md's index the script fetches the page,
records a SHA-256 of its normalized text, checks that the expected publication
date appears, and checks that every claim listed in claims.tsv for that article
appears verbatim in the page text. A report is written to report.md and the exit
code is 1 if any check fails.
"""
import argparse, hashlib, html, json, os, re, ssl, sys, urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "..", "IMPLEMENTATION_PLAN.md")
CLAIMS = os.path.join(HERE, "claims.tsv")
REPORT = os.path.join(HERE, "report.md")
MIRROR = "https://raw.githubusercontent.com/ai-native-engineer/anthropic-mirror/main/www.anthropic.com/engineering/{slug}.md"
# Per-slug overrides for posts the primary archive lacks (see mirror_overrides.json).
OVERRIDES = os.path.join(HERE, "mirror_overrides.json")
# claude-code-best-practices now serves the living docs page, which has no "Published" line.
NO_DATE = {"claude-code-best-practices"}

def load_index():
    rows = []
    for line in open(PLAN, encoding="utf-8"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)\s*\|\s*https://www\.anthropic\.com/engineering/([\w-]+)\s*\|", line)
        if m:
            rows.append({"n": int(m.group(1)), "date": m.group(2), "title": m.group(3), "slug": m.group(4)})
    return rows

def load_claims():
    claims = {}
    for line in open(CLAIMS, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        slug, text = parts[0], parts[1]
        live_only = len(parts) > 2 and parts[2].strip() == "live"
        claims.setdefault(slug, []).append((text, live_only))
    return claims

def normalize(text):
    text = html.unescape(text)
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("—", "-").replace("–", "-").replace(" ", " ").replace("×", "x")
    return re.sub(r"\s+", " ", text)

def strip_html(raw):
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return raw

def fetch(url, ca_bundle):
    ctx = ssl.create_default_context(cafile=ca_bundle) if ca_bundle else None
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (verify_live.py)"})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        return r.read().decode("utf-8", errors="replace")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["live", "mirror"], default="live")
    ap.add_argument("--ca-bundle", default=os.environ.get("VERIFY_CA_BUNDLE"))
    ap.add_argument("--only", help="comma-separated slugs to check")
    ap.add_argument("--report", default=REPORT, help="where to write the Markdown report (JSON goes alongside)")
    args = ap.parse_args()

    index, claims = load_index(), load_claims()
    only = set(args.only.split(",")) if args.only else None
    results, failures = [], 0
    for row in index:
        slug = row["slug"]
        if only and slug not in only:
            continue
        overrides = json.load(open(OVERRIDES)) if os.path.exists(OVERRIDES) else {}
        url = f"https://www.anthropic.com/engineering/{slug}" if args.source == "live" else overrides.get(slug, MIRROR.format(slug=slug))
        entry = {"n": row["n"], "slug": slug, "url": url, "date": row["date"]}
        try:
            raw = fetch(url, args.ca_bundle)
        except Exception as e:  # noqa: BLE001
            entry.update(status="fetch-failed", error=str(e)[:200])
            results.append(entry); failures += 1
            continue
        text = normalize(strip_html(raw) if args.source == "live" else raw)
        entry["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        d = date.fromisoformat(row["date"])
        date_forms = [f"{d.strftime('%b')} {d.day}, {d.year}", f"{d.strftime('%b')} {d.day:02d}, {d.year}",
                      f"{d.strftime('%B')} {d.day}, {d.year}", f"{d.strftime('%B')} {d.day:02d}, {d.year}"]
        # Posts that now redirect to a docs page carry no publication line.
        entry["date_found"] = True if slug in NO_DATE else any(f in text for f in date_forms)
        checks = []
        for c, live_only in claims.get(slug, []):
            if live_only and args.source != "live":
                continue  # matches only the live HTML rendering, not the markdown archive
            checks.append({"claim": c, "found": normalize(c) in text})
        entry["claims"] = checks
        missing = [c for c in checks if not c["found"]]
        entry["status"] = "ok" if entry["date_found"] and not missing else "mismatch"
        if entry["status"] != "ok":
            failures += 1
        results.append(entry)

    with open(args.report, "w", encoding="utf-8") as f:
        f.write(f"# Live verification report\n\nSource: {args.source}. Run date: {date.today().isoformat()}.\n\n")
        f.write("| # | Article | Status | Date found | Claims found | SHA-256 |\n|---|---------|--------|------------|--------------|---------|\n")
        for e in results:
            n_ok = sum(1 for c in e.get("claims", []) if c["found"]); n_all = len(e.get("claims", []))
            f.write(f"| {e['n']} | {e['slug']} | {e['status']} | {e.get('date_found', '-')} | {n_ok}/{n_all} | {e.get('sha256', '-')[:16]} |\n")
        f.write("\n## Missing claims\n\n")
        any_missing = False
        for e in results:
            for c in e.get("claims", []):
                if not c["found"]:
                    any_missing = True
                    f.write(f"- {e['slug']}: `{c['claim']}`\n")
            if e.get("status") == "fetch-failed":
                any_missing = True
                f.write(f"- {e['slug']}: fetch failed: {e['error']}\n")
        if not any_missing:
            f.write("None.\n")
    json.dump(results, open(os.path.splitext(args.report)[0] + ".json", "w"), indent=2)
    print(open(args.report, encoding="utf-8").read())
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
