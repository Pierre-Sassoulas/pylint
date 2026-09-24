"""Extract code blocks + suggested pylint command from an issue body."""

import json
import re
import sys

with open("/home/pierre/pylint/.triage/issues_raw.json") as f:
    ISSUES = {i["number"]: i for i in json.load(f)}

CODE_RE = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)
SHELL_RE = re.compile(r"```(?:shell|bash|sh|console)\n(.*?)```", re.DOTALL)


def extract(num):
    issue = ISSUES.get(num)
    if not issue:
        return None
    body = issue["body"] or ""
    blocks = []
    for m in CODE_RE.finditer(body):
        lang = (m.group(1) or "").lower()
        code = m.group(2).strip()
        blocks.append({"lang": lang, "code": code})
    return {"issue": issue, "blocks": blocks}


def main():
    for arg in sys.argv[1:]:
        num = int(arg)
        e = extract(num)
        if not e:
            print(f"#{num}: NOT FOUND")
            continue
        i = e["issue"]
        print(f"\n=== #{i['number']}: {i['title']}")
        print(f"created={i['created_at'][:10]} labels={','.join(i['labels'])}")
        print(f"url={i['html_url']}")
        py = [b for b in e["blocks"] if b["lang"] in ("python", "py", "")]
        sh = [b for b in e["blocks"] if b["lang"] in ("shell", "bash", "sh", "console")]
        ini = [b for b in e["blocks"] if b["lang"] in ("ini", "toml", "cfg")]
        print(f"blocks: {len(e['blocks'])} (py={len(py)} sh={len(sh)} cfg={len(ini)})")
        for j, b in enumerate(py):
            print(f"--- python block {j} ---")
            print(b["code"][:1500])
        for j, b in enumerate(sh):
            print(f"--- shell block {j} ---")
            print(b["code"][:500])
        for j, b in enumerate(ini):
            print(f"--- cfg block {j} ---")
            print(b["code"][:500])


if __name__ == "__main__":
    main()
