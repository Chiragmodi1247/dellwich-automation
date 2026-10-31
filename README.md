# dellwich-automation

Small tools for opening a batch of links at once.

## Web page (`public/index.html`)

A single static page with no build step and no dependencies.

1. Paste any text, such as a WhatsApp chat export.
2. The page finds every link and removes duplicates.
3. Click **Open all** to open each link in a new tab, or **Open next** to go one at a time.

The first time you use it, Chrome blocks every tab after the first one. Click the pop-up icon in the address bar, choose **Always allow pop-ups** for the site, and try again.

### Deploy on GitHub Pages (free)

Go to **Settings → Pages**, choose **Deploy from a branch**, then pick `main` and `/ (root)`.
The page is then live at `https://chiragmodi1247.github.io/dellwich-automation/public/`.

### Deploy on Firebase Hosting (GCP free tier)

```bash
npm install -g firebase-tools
firebase login
firebase use --add            # pick or create your GCP/Firebase project
firebase deploy --only hosting
```

## Local script (`scripts/open_links_in_chrome.py`)

macOS only. It opens links in Google Chrome on your machine.

```bash
python3 scripts/open_links_in_chrome.py             # opens the built-in list
python3 scripts/open_links_in_chrome.py chat.txt    # finds the links in a text file
```
