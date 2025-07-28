# JustApply - Job Scraper

A smart tool for monitoring job listings websites for changes by periodically scraping them and recording differences. Currently tracks internship and early career opportunities in Singapore from major tech and finance companies.

## Features

- 🔄 **Automated scraping** using Selenium with headless Chrome
- 📱 **Telegram notifications** for instant updates when changes are detected
- 📊 **Smart change detection** that compares text content line by line
- 📝 **Clean output** with only the latest changes (no historical clutter)
- 🌐 **JavaScript support** - waits for dynamic content to load
- 🎯 **Focused monitoring** - currently tracks internship opportunities from:
  - Stripe
  - Google
  - Meta
  - Apple
  - Squarepoint Capital

## Installation

### Prerequisites
- Python 3.11 or higher
- Google Chrome browser
- Git

### Quick Setup

1. **Clone this repository:**
   ```bash
   git clone <repository-url>
   cd JustApply
   ```

2. **Set up virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the setup:**
   ```bash
   python daily_scraper.py
   ```

## Configuration

### Setting Up Telegram Notifications

To receive instant notifications when changes are detected:

1. **Follow the setup guide**: See `TELEGRAM_SETUP.md` for detailed instructions
2. **Add GitHub secrets**:
   - `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather
   - `TELEGRAM_CHAT_ID` - Your personal chat ID

### Customizing the Scraper

Edit the `daily_scraper.py` file to customize:

1. **URLs to monitor**: Modify the `urls` list in the `main()` function
2. **Wait time**: Adjust `time.sleep()` in `fetch_page()` if pages load slowly
3. **Browser visibility**: Comment/uncomment `--headless` in `setup_selenium()` for testing

## Usage

### Manual Run

Run the script locally to check for changes:

```bash
python daily_scraper.py
```

The script will:
1. 🌐 Load each configured URL using Chrome browser
2. ⏱️ Wait for the page to fully load (including JavaScript)
3. 📄 Extract the text content, removing HTML markup and scripts
4. 🔍 Compare with the previously saved version
5. 📝 Record any changes in `changes.md` with a timestamp
6. 📱 Send Telegram notification if changes are detected

### Automated Daily Checks

The repository includes a GitHub Actions workflow that automatically runs the scraper daily. The workflow:

1. 🕐 Runs every day at 07:00 UTC (`cron: "0 7 * * *"`)
2. 🚀 Can be triggered manually using the "Run workflow" button
3. 🐍 Sets up Python 3.11 and installs required dependencies
4. 🔄 Runs the scraper script
5. 📱 Sends Telegram notification if changes are detected
6. 💾 Commits and pushes any changes to the repository

**To enable automated checks:**
1. Fork this repository
2. Go to the "Actions" tab
3. Enable GitHub Actions for your fork
4. Set up Telegram notifications (see `TELEGRAM_SETUP.md`)
5. The workflow will automatically run daily

**The workflow will:**
- ✅ Create a new commit with any detected changes
- 📝 Update the `changes.md` file with latest results only
- 💾 Update the `text_storage` directory with new content
- 📱 Send Telegram notification with change details
- 🔄 Commit message: "🔄 Daily scrape update: YYYY-MM-DD HH:MM:SS UTC"

### First Run Behavior

**Important**: The first time you run the script for a URL, it will save the current content but won't show any meaningful changes (as there's nothing to compare against). The script will report:

```
Changes detected for [URL]
No previous version found
```

This is expected behavior. The script needs to establish a baseline before it can detect changes. For new job sites you add:

1. Run the script once to capture the initial state
2. Visit the site manually to check current listings
3. Run the script again on subsequent days to detect changes

The real value comes from running the script regularly (e.g., daily) after the initial run, as it will then show you exactly what changed on the job listings page since the last check.

## Output

### File Structure

```
JustApply/
├── daily_scraper.py          # Main scraper script
├── requirements.txt          # Python dependencies
├── changes.md               # Latest scraping results
├── text_storage/            # Stored text content (one file per URL)
│   ├── [hash1].txt
│   ├── [hash2].txt
│   └── ...
├── .github/workflows/       # GitHub Actions automation
│   └── daily_scrape.yml
└── TELEGRAM_SETUP.md        # Telegram notification setup guide
```

### Changes Log

Changes are recorded in `changes.md` with only the latest results (no historical clutter). For each run, the file shows:

- 📅 Timestamp for when the check was performed
- 🔗 URLs that were checked
- ✅ Status for each URL (changes detected or no changes)
- 📊 For changed pages, a diff showing what content was added/removed

**Example output:**
```markdown
# Latest Scraper Results

## 2023-09-15 10:30:45

### [https://stripe.com/jobs/search?office_locations=Asia+Pacific--Singapore&tags=University](https://stripe.com/jobs/search?office_locations=Asia+Pacific--Singapore&tags=University)

**Line changes detected!**

```diff
+ Software Engineering Intern
+ Data Science Intern
- Previous Internship Position
```

---

### Telegram Notifications

When changes are detected, you'll receive a formatted message like:

```
🔄 Daily Scraper Update

Changes detected:
Software Engineering Intern
Data Science Intern
Previous Internship Position

Updated at: 2023-09-15 10:30:45 UTC
```

## Advanced Usage

### Adding New Sites

To add a new job site to monitor, add its URL to the `urls` list in the `main()` function:

```python
def main():
    urls = [
        "https://stripe.com/jobs/search?office_locations=Asia+Pacific--Singapore&tags=University",
        "https://new-site.com/careers"  # Add your new site here
    ]
```

### Customizing Text Extraction

The `extract_text()` function uses BeautifulSoup to:
1. 🧹 Remove all script and style tags
2. 📄 Extract text content with line breaks between blocks
3. ✨ Normalize whitespace and remove empty lines

You can modify this function if certain sites require special handling.

### Testing Mode

For debugging, you can run the scraper with a visible browser:

1. **Edit `daily_scraper.py`** and comment out the headless option:
```python
def setup_selenium():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Comment this line for testing
    # ... rest of the function
```

2. **Run the scraper** to see the browser in action:
```bash
python daily_scraper.py
```

## Troubleshooting

### Common Issues

- **ChromeDriver issues**: The script uses webdriver-manager to automatically download the correct ChromeDriver version. If you encounter issues, try running with the `--headless` option removed to see the browser in action.

- **Website blocking**: Some websites may block automated access. Consider adding more realistic user agent strings or other headers as needed.

- **Long load times**: If the page content is not fully loaded before capturing, increase the `time.sleep()` value in the `fetch_page()` function (currently 15 seconds).

- **Virtual environment issues**: Make sure you see `(venv)` in your terminal prompt. If not, activate it:
  ```bash
  # Windows
  venv\Scripts\activate
  
  # macOS/Linux
  source venv/bin/activate
  ```

### GitHub Actions Issues

If the workflow fails, check the Actions tab for error messages. Common issues include:
- Rate limiting from job sites
- Changes in website structure
- Network connectivity issues
- Missing Telegram secrets (if notifications are enabled)

### Telegram Notification Issues

- **Bot not responding**: Make sure you've started a chat with your bot
- **"Forbidden" error**: Check that your chat ID is correct
- **No notifications**: Verify both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` secrets are set

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).