import feedparser
import re
import hashlib
from pathlib import Path

FEED_URL = "https://TheLastAnalogue.substack.com/feed"
OUTPUT_DIR = Path("essays")
OUTPUT_DIR.mkdir(exist_ok=True)

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80]

def hash_content(content):
    return hashlib.md5(content.encode("utf-8")).hexdigest()

feed = feedparser.parse(FEED_URL)

for entry in feed.entries:
    title = entry.title
    date = entry.published
    link = entry.link

    content = entry.get("content", [{}])[0].get("value", "")
    content_hash = hash_content(content)

    filename = f"{slugify(title)}.md"
    filepath = OUTPUT_DIR / filename

    if filepath.exists():
        existing = filepath.read_text(encoding="utf-8")
        if content_hash in existing:
            continue

    md = f"""---
title: {title}
date: {date}
source: {link}
hash: {content_hash}
---

# {title}

{content}
"""

    filepath.write_text(md, encoding="utf-8")

print("Sync complete.")
