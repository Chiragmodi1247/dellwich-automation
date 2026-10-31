# dellwich-automation

Small tools for opening a batch of links at once.

## Web page (`public/index.html`)

A single static page with no build step and no dependencies.

The default links live in `public/links.txt`. The page loads them on first visit, and **Load saved links** brings them back at any time. To change the defaults, edit `links.txt`, commit, and push.

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
python3 scripts/open_links_in_chrome.py             # opens public/links.txt
python3 scripts/open_links_in_chrome.py chat.txt    # finds the links in a text file
```

## Background job on macOS (every 30 minutes)

This opens the links on a schedule even when the web page is closed. It runs as a macOS launchd job, which macOS starts by itself.

```bash
./scripts/install_mac_scheduler.sh            # every 30 minutes
./scripts/install_mac_scheduler.sh 15         # pick another interval
./scripts/install_mac_scheduler.sh uninstall  # stop it
```

- Each run reads `public/links.txt` from GitHub, so pushing a change to the list updates what opens. When offline, it uses the local copy saved at install time.
- A link that is already open in a Chrome tab is reloaded instead of opened again.
- The first run asks for permission to control Chrome. If you miss that prompt, enable it under System Settings → Privacy & Security → Automation.
- No runs happen while the laptop is asleep. One run happens shortly after it wakes up.
- Log: `~/Library/Application Support/dellwich-automation/run.log`
