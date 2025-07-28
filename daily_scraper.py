from datetime import datetime
from typing import Tuple
import os
import hashlib
import difflib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup


def get_url_hash(url: str) -> str:
    """Generate a unique hash for the URL to use as filename"""
    return hashlib.md5(url.encode()).hexdigest()


def setup_selenium():
    """Set up and return a configured Chrome WebDriver using webdriver-manager"""
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Comment this line out for testing
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Automatically download and use the correct chromedriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def fetch_page(url: str) -> str | None:
    print(f"🌐 Fetching page content from {url}")
    driver = None
    try:
        driver = setup_selenium()
        driver.get(url)

        # Wait for the page to load with a fixed delay
        print("Waiting 5 seconds for page to load and JavaScript to execute...")
        time.sleep(15)

        # Get the page source after JavaScript execution
        html_content = driver.page_source
        print("Page fetched successfully with Selenium")
        return html_content

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    finally:
        if driver:
            driver.quit()


def save_text(url: str, text_content: str) -> None:
    """Save extracted text content to a file"""
    if not text_content:
        return

    # Create text_storage directory if it doesn't exist
    os.makedirs('text_storage', exist_ok=True)

    # Generate filename from URL
    filename = f"text_storage/{get_url_hash(url)}.txt"

    # Save the text content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text_content)

    print(f"Saved text for {url} to {filename}")


def extract_text(html: str) -> str:
    """Extract user-visible text content from HTML with structured line breaks"""
    soup = BeautifulSoup(html, 'html.parser')

    # Remove non-visible elements
    for tag in soup(['script', 'style']):
        tag.decompose()

    # Get text with line breaks between blocks
    text = soup.get_text(separator='\n')  # This is the key change

    # Normalize whitespace and remove empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)


def get_text_diff(old_text: str, new_text: str) -> str:
    """Generate a diff of line additions and removals between two text contents, diff-style."""
    from collections import Counter
    # Split by newlines
    old_lines = [line.strip() for line in old_text.splitlines() if line.strip()]
    new_lines = [line.strip() for line in new_text.splitlines() if line.strip()]
    old_counts = Counter(old_lines)
    new_counts = Counter(new_lines)

    all_lines = sorted(set(old_counts) | set(new_counts))
    diff_lines = []
    for line in all_lines:
        old_count = old_counts.get(line, 0)
        new_count = new_counts.get(line, 0)
        if old_count == new_count:
            continue
        if new_count > old_count:
            # Added lines
            count = new_count - old_count
            prefix = '+ '
            suffix = f' x{count}' if count > 1 else ''
            diff_lines.append(f'{prefix}{line}{suffix}')
        elif old_count > new_count:
            # Removed lines
            count = old_count - new_count
            prefix = '- '
            suffix = f' x{count}' if count > 1 else ''
            diff_lines.append(f'{prefix}{line}{suffix}')
    if not diff_lines:
        return "No line changes."
    return '\n'.join(diff_lines)


def has_text_changed(url: str, new_text: str) -> Tuple[bool, str]:
    """Check if the word count of the text content has changed from the stored version and return the word-count diff if changed"""
    filename = f"text_storage/{get_url_hash(url)}.txt"

    # If file doesn't exist, it's considered changed
    if not os.path.exists(filename):
        return True, "No previous version found"

    # Read stored text
    with open(filename, 'r', encoding='utf-8') as f:
        stored_text = f.read()

    # Compare text directly (word count based)
    if stored_text != new_text:
        if stored_text.strip() or new_text.strip():
            diff = get_text_diff(stored_text, new_text)
            return True, diff

    return False, ""


def append_to_markdown(results: list[tuple[str, bool, str]]) -> None:
    """Replace the markdown log file with the latest changes only"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create new content
    new_content = f"# Latest Scraper Results\n\n## {timestamp}\n\n"

    # Check if any URLs have changes
    has_any_changes = any(has_changes for _, has_changes, _ in results)

    if has_any_changes:
        # Only show URLs that have changes
        for url, has_changes, diff in results:
            if has_changes:
                new_content += f"### [{url}]({url})\n\n"  # Use markdown link format
                new_content += "**Line changes detected!**\n\n"
                new_content += "```diff\n"
                new_content += diff
                new_content += "\n```\n"
                new_content += "\n---\n"
    else:
        # If no changes detected for any URL, show a single message
        new_content += "**No changes for today**\n\n---\n"

    # Write new content, completely replacing the file
    with open('changes.md', 'w', encoding='utf-8') as f:
        f.write(new_content)


def process_urls(urls: list[str]) -> None:
    """Process URLs and store their text content"""
    results = []

    for url in urls:
        print(f"\nProcessing URL: {url}")
        if html_content := fetch_page(url):
            # Extract text from HTML
            text_content = extract_text(html_content)

            has_changed, diff = has_text_changed(url, text_content)
            if has_changed:
                print(f"Changes detected for {url}")
                save_text(url, text_content)
            else:
                print(f"No changes detected for {url}")

            results.append((url, has_changed, diff))
        else:
            print(f"Failed to fetch content from {url}")
            results.append((url, False, "Failed to fetch content"))

    # Append all results with a single timestamp
    append_to_markdown(results)


def main():
    urls = [
        "https://stripe.com/jobs/search?office_locations=Asia+Pacific--Singapore&tags=University",
        "https://www.google.com/about/careers/applications/jobs/results/?src=Online%2FGoogle%20Website%2FByF&utm_source=Online%20&utm_medium=careers_site%20&utm_campaign=ByF&distance=50&employment_type=INTERN&company=Fitbit&company=Google&location=Singapore",
        "https://www.metacareers.com/jobs?offices[0]=Singapore&roles[0]=Internship",
        "https://jobs.apple.com/en-us/search?location=singapore-SGP&team=internships-STDNT-INTRN",
        "https://www.squarepoint-capital.com/open-opportunities?id=6212106",
    ]

    process_urls(urls)
    print("\nText storage and comparison completed. Check changes.md for the log.")


if __name__ == "__main__":
    main()