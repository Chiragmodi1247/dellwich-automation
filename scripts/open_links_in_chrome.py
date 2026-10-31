#!/usr/bin/env python3
"""Open a list of links in Google Chrome (macOS).

Usage:
    python3 open_links_in_chrome.py              # opens the links in LINKS below
    python3 open_links_in_chrome.py links.txt    # pulls every URL out of a text file
                                                 # (e.g. a pasted WhatsApp chat)
"""

import re
import subprocess
import sys
import time

LINKS = """
https://dellwich.com/paroxetine-cr-clonazepam-tablet-25-mg-paxotin-cr-forte/
https://dellwich.com/paroxetine-cr-clonazepam-tablet-12-5-mg-paxotin-cr-plus/
https://dellwich.com/propranolol-alprazolam-tablet-migabet-plus/
https://dellwich.com/lorazepam-injection-2-mg-ml-lorzin/
https://dellwich.com/lorazepam-tablet-3-mg-lorzin-3/
https://dellwich.com/lorazepam-tablet-2-mg-lorzin-2/
https://dellwich.com/lorazepam-tablet-1-mg-lorzin-1/
https://dellwich.com/escitalopram-etizolam-tablet-10-mg-esicare-ez/
https://dellwich.com/escitalopram-clonazepam-tablet-10-mg-esicare-plus/
https://dellwich.com/escitalopram-clonazepam-tablet-10-mg-esicare-ls/
https://dellwich.com/escitalopram-clonazepam-tablet-5-mg-esicare-plus-h/
https://dellwich.com/clonazepam-melatonin-tablet-delotril-plus-5/
https://dellwich.com/clonazepam-propranolol-tablet-delotril-pro-0-5/
https://dellwich.com/clonazepam-propranolol-tablet-delotril-pro-0-25/
https://dellwich.com/clonazepam-propranolol-tablet-delotril-pro-ls/
https://dellwich.com/clonazepam-md-tablet-2-mg-delotril/
https://dellwich.com/clonazepam-md-tablet-1-mg-delotril/
https://dellwich.com/clonazepam-md-tablet-0-5-mg-delotril/
https://dellwich.com/clonazepam-md-tablet-0-25-mg-delotril/
https://dellwich.com/diazepam-tablet-10-mg-d-cam-10/
https://dellwich.com/diazepam-tablet-5-mg-d-cam-5/
https://dellwich.com/clobazam-tablet-10-mg-cliba-10/
https://dellwich.com/clobazam-tablet-5-mg-cliba-5/
https://dellwich.com/phenobarbitone-tablet-60-mg-barzox-60/
https://dellwich.com/phenobarbitone-30-mg-barzox-30-blessme-neuro-product/
"""

DELAY_SECONDS = 0.3  # small pause so Chrome isn't flooded


def extract_urls(text):
    """Find every http(s) URL in the text, de-duplicated, in order."""
    urls = re.findall(r"https?://[^\s<>\"']+", text)
    return list(dict.fromkeys(urls))


def main():
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else LINKS
    urls = extract_urls(text)
    if not urls:
        print("No links found.")
        return

    print(f"Opening {len(urls)} links in Chrome...")
    for i, url in enumerate(urls, 1):
        subprocess.run(["open", "-a", "Google Chrome", url], check=True)
        print(f"  [{i}/{len(urls)}] {url}")
        time.sleep(DELAY_SECONDS)
    print("Done.")


if __name__ == "__main__":
    main()
