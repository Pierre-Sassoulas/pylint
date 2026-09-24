"""Print an issue's metadata + body from the cache."""

import json
import sys

with open("/home/pierre/pylint/.triage/issues_raw.json") as f:
    issues = json.load(f)
nums = [int(a) for a in sys.argv[1:]]
for n in nums:
    issue = next((i for i in issues if i["number"] == n), None)
    if not issue:
        print(f"#{n}: NOT FOUND")
        continue
    print(f"=== #{issue['number']}: {issue['title']}")
    print(
        f"created={issue['created_at'][:10]} updated={issue['updated_at'][:10]} comments={issue['comments']}"
    )
    print(f"labels: {', '.join(issue['labels']) or '(none)'}")
    print(f"author: {issue['user']}")
    print(f"url: {issue['html_url']}")
    print("---")
    print(issue["body"][:4000])
    if len(issue["body"]) > 4000:
        print(f"\n[...truncated {len(issue['body'])-4000} chars]")
    print()
