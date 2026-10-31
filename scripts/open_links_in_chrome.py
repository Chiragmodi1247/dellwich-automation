#!/usr/bin/env python3
"""Open a list of links in Google Chrome (macOS).

Usage:
    python3 scripts/open_links_in_chrome.py                  # opens public/links.txt
    python3 scripts/open_links_in_chrome.py chat.txt         # any text file (e.g. a WhatsApp chat)
    python3 scripts/open_links_in_chrome.py https://.../links.txt   # a file on the web
    python3 scripts/open_links_in_chrome.py --new-tabs       # always open new tabs

By default, a link that is already open in Chrome gets reloaded instead of
opening a duplicate tab, so running this on a schedule doesn't pile up tabs.
The first run asks for permission to control Chrome (System Settings >
Privacy & Security > Automation).

You can pass several sources: the first one that works is used. This lets the
background job try GitHub first and fall back to a local copy when offline.
"""

import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

DEFAULT_LINKS_FILE = Path(__file__).resolve().parent.parent / "public" / "links.txt"
DELAY_SECONDS = 0.3  # small pause so Chrome isn't flooded

# Reload each link if a tab already shows it, otherwise open it in a new tab.
REUSE_TABS_SCRIPT = """
on run argv
    tell application "Google Chrome"
        if (count of windows) = 0 then make new window
        repeat with u in argv
            set u to u as text
            set found to false
            repeat with w in windows
                repeat with t in tabs of w
                    if (URL of t) starts with u then
                        tell t to reload
                        set found to true
                        exit repeat
                    end if
                end repeat
                if found then exit repeat
            end repeat
            if not found then
                tell window 1 to make new tab with properties {URL:u}
            end if
            delay %s
        end repeat
    end tell
end run
""" % DELAY_SECONDS


def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def extract_urls(text):
    """Find every http(s) URL in the text, de-duplicated, in order."""
    urls = re.findall(r"https?://[^\s<>\"']+", text)
    return list(dict.fromkeys(urls))


def read_source(source):
    if re.match(r"https?://", source):
        with urllib.request.urlopen(source, timeout=15) as res:
            return res.read().decode("utf-8")
    return Path(source).read_text(encoding="utf-8")


def load_urls(sources):
    for source in sources:
        try:
            urls = extract_urls(read_source(source))
        except Exception as e:  # network down, file missing, etc.
            log(f"Couldn't read {source}: {e}")
            continue
        if urls:
            log(f"Loaded {len(urls)} links from {source}")
            return urls
    return []


def open_new_tabs(urls):
    for i, url in enumerate(urls, 1):
        subprocess.run(["open", "-a", "Google Chrome", url], check=True)
        log(f"  [{i}/{len(urls)}] {url}")
        time.sleep(DELAY_SECONDS)


def open_reusing_tabs(urls):
    subprocess.run(["osascript", "-e", REUSE_TABS_SCRIPT, *urls], check=True)
    log(f"Opened or reloaded {len(urls)} links")


def main():
    args = sys.argv[1:]
    new_tabs = "--new-tabs" in args
    sources = [a for a in args if a != "--new-tabs"] or [str(DEFAULT_LINKS_FILE)]

    urls = load_urls(sources)
    if not urls:
        log("No links found.")
        sys.exit(1)

    if new_tabs:
        open_new_tabs(urls)
    else:
        open_reusing_tabs(urls)


if __name__ == "__main__":
    main()
