#!/usr/bin/env python3
"""Open a list of links in Google Chrome (macOS).

Usage:
    python3 scripts/open_links_in_chrome.py              # opens public/links.txt
    python3 scripts/open_links_in_chrome.py chat.txt     # pulls every URL out of any text file
                                                         # (e.g. a pasted WhatsApp chat)
"""

import re
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_LINKS_FILE = Path(__file__).resolve().parent.parent / "public" / "links.txt"
DELAY_SECONDS = 0.3  # small pause so Chrome isn't flooded


def extract_urls(text):
    """Find every http(s) URL in the text, de-duplicated, in order."""
    urls = re.findall(r"https?://[^\s<>\"']+", text)
    return list(dict.fromkeys(urls))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LINKS_FILE
    urls = extract_urls(path.read_text(encoding="utf-8"))
    if not urls:
        print(f"No links found in {path}.")
        return

    print(f"Opening {len(urls)} links in Chrome...")
    for i, url in enumerate(urls, 1):
        subprocess.run(["open", "-a", "Google Chrome", url], check=True)
        print(f"  [{i}/{len(urls)}] {url}")
        time.sleep(DELAY_SECONDS)
    print("Done.")


if __name__ == "__main__":
    main()
