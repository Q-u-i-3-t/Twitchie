# UwU~! Twitch Streamer Scanner & StreamElements Command Checker desu! >w<

Kyaa~! A collection of Python scripts to find streamers and check their commands nya~! ✨

A collection of Python scripts to:
1. UwU~! Scan Twitch.tv for active streamers desu! >w<
2. Kyaa~! Check StreamElements commands for streamers with specific criteria nya~! ✨

## Requirements desu~!

- Python 3.7+ (so important desu! >w<)
- Chrome browser installed (the browser thingy nya~!)
- ChromeDriver (compatible with your Chrome version - so cute desu~!)

## Installation nya~! ✨

1. UwU~! Install Python dependencies desu! >w<
```bash
pip install -r requirements.txt
```

2. Kyaa~! Install ChromeDriver nya~! ✨
   - Download from: https://chromedriver.chromium.org/
   - Or use a package manager:
     - Windows (with Chocolatey): `choco install chromedriver`
     - macOS (with Homebrew): `brew install chromedriver`
     - Linux: `sudo apt-get install chromium-chromedriver` (or equivalent)

## Usage desu! >w<

### Step 1: UwU~! Scan for Active Streamers nya~! ✨

Run the first script to get a list of active Twitch streamers:
```bash
python scan_twitch_streamers.py
```

Or limit the number of categories to scan (useful for testing):
```bash
python scan_twitch_streamers.py 50
```

Kyaa~! The script will:
1. UwU~! Load the Twitch directory to discover all categories/games desu! >w<
2. Kyaa~! Visit each category page and extract active streamers nya~! ✨
3. UwU~! Also scan the homepage for additional streamers desu! >w<
4. Kyaa~! Extract streamer handles/usernames from all sources nya~! ✨
5. UwU~! Save unique streamer handles to `twitch_streamers.txt` desu! >w<

**Note:** Scanning all categories can take a while. The script shows progress as it processes each category. So exciting desu~!

### Step 2: Kyaa~! Check StreamElements Commands nya~! ✨

After generating the streamer list, run the second script to check their StreamElements commands:
```bash
python check_streamelements_commands.py
```

UwU~! This script will:
1. Kyaa~! Read streamer usernames from `twitch_streamers.txt` nya~! ✨
2. UwU~! Visit each streamer's StreamElements commands page: `https://streamelements.com/{username}/commands` desu! >w<
3. Kyaa~! Look for commands that have:
   - `$(touser)` in the response (so important desu~!)
   - Permissions set to "Everyone" (everyone can use it nya~!)
4. UwU~! Save matching streamers with their command names and responses to `streamelements_streamers.txt` desu! >w<

## Output desu~!

### Step 1 Output
- `twitch_streamers.txt`: Text file with one streamer handle per line, sorted alphabetically (so organized desu! >w<)

### Step 2 Output
- `streamelements_streamers.txt`: Text file with streamer usernames and their matching commands
  - Format: Streamer username on one line, followed by command name and response on the next line
  - Example:
    ```
    joe_bartolozzi
    !ban Banned $(touser) !!!
    
    streamer2
    !repeat $(touser)
    ```
  - Only includes streamers who use StreamElements AND have at least one command with `$(touser)` in the response AND "Everyone" permissions (so specific desu~!)

## Notes nya~! ✨

- UwU~! Both scripts run in headless mode (no browser window will appear) desu! >w<
- Kyaa~! The streamer scanner now scans **all Twitch categories**, not just the homepage, for comprehensive coverage nya~! ✨
- UwU~! Scanning all categories can take 30+ minutes depending on the number of categories found (so much waiting desu~!)
- Kyaa~! You can limit the scan with a command-line argument: `python scan_twitch_streamers.py 50` (scans first 50 categories) nya~!
- UwU~! The StreamElements checker includes delays between requests to avoid overwhelming servers (so polite desu! >w<)
- Kyaa~! If scripts don't find expected data, the page structures may have changed and selectors may need updating nya~! ✨
- UwU~! For more comprehensive results, consider using the official Twitch API or StreamElements API desu! >w<
- Kyaa~! The script can be interrupted (Ctrl+C) and will save partial results (so helpful nya~!)

Reading all this shit gave me cancer. Thanks for making it... Whatever the fuck this is, clankers.
