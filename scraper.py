#!/usr/bin/env python3
"""
Web Scraper
===========

A simple command-line web scraper built with `requests` and `BeautifulSoup4`.

The script asks the user for a URL, fetches the page, extracts useful
information (title, metadata, headings, links, images, and readable text),
prints a formatted report to the terminal, and optionally saves the report
to a plain-text file at a user-supplied path.

Author: ryzoru1
License: GNU General Public License v3.0
"""

import os
import sys
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# A realistic User-Agent so most websites do not reject the request outright.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

# Seconds to wait before giving up on a slow server.
REQUEST_TIMEOUT = 15

# Maximum number of links / images to list in the report so the output
# stays readable for very large pages.
MAX_LISTED_ITEMS = 50


def print_banner():
    """Print a small welcome banner."""
    print("=" * 60)
    print("              Python Web Scraper (BeautifulSoup4)")
    print("=" * 60)


def normalize_url(raw_url):
    """Add a scheme to the URL if the user omitted it."""
    raw_url = raw_url.strip()
    if not raw_url:
        return None
    if not urlparse(raw_url).scheme:
        raw_url = "https://" + raw_url
    return raw_url


def ask_for_url():
    """Prompt the user until a syntactically valid URL is entered."""
    while True:
        raw = input("\nEnter the URL of the website to scrape: ").strip()
        url = normalize_url(raw)
        if not url:
            print("[!] Please enter a non-empty URL.")
            continue
        parsed = urlparse(url)
        if parsed.netloc == "" or "." not in parsed.netloc:
            print("[!] That does not look like a valid URL. Try again.")
            continue
        return url


def fetch_page(url):
    """Download the page and return an HTML string, or None on failure."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.exceptions.MissingSchema:
        print("[!] Invalid URL format.")
    except requests.exceptions.ConnectionError:
        print("[!] Connection failed. Check the URL and your internet connection.")
    except requests.exceptions.Timeout:
        print(f"[!] The server took too long to respond (timeout {REQUEST_TIMEOUT}s).")
    except requests.exceptions.HTTPError as exc:
        print(f"[!] HTTP error: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"[!] Request failed: {exc}")
    return None


def build_soup(html, url):
    """Parse HTML and resolve the base URL for converting relative links."""
    soup = BeautifulSoup(html, "html.parser")
    base = soup.find("base", href=True)
    if base:
        return soup, urljoin(url, base["href"])
    return soup, url


def extract_data(soup, base_url):
    """Pull all interesting pieces of information out of the parsed page."""
    data = {}

    data["title"] = soup.title.get_text(strip=True) if soup.title else "(no title found)"

    description = soup.find("meta", attrs={"name": "description"})
    keywords = soup.find("meta", attrs={"name": "keywords"})
    data["description"] = description["content"].strip() if description and description.get("content") else "(none)"
    data["keywords"] = keywords["content"].strip() if keywords and keywords.get("content") else "(none)"

    headings = {level: [] for level in ("h1", "h2", "h3")}
    for level in headings:
        for tag in soup.find_all(level):
            text = tag.get_text(strip=True)
            if text:
                headings[level].append(text)
    data["headings"] = headings

    links = []
    seen = set()
    for anchor in soup.find_all("a", href=True):
        absolute = urljoin(base_url, anchor["href"].strip())
        if absolute.startswith(("http://", "https://")) and absolute not in seen:
            seen.add(absolute)
            links.append(absolute)
    data["links"] = links

    images = []
    seen_imgs = set()
    for img in soup.find_all("img", src=True):
        absolute = urljoin(base_url, img["src"].strip())
        if absolute not in seen_imgs:
            seen_imgs.add(absolute)
            images.append(absolute)
    data["images"] = images

    for unwanted in soup(["script", "style", "noscript", "template", "svg"]):
        unwanted.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    data["text"] = "\n".join(line for line in lines if line)

    return data


def section(report, heading):
    """Append a section header to the report."""
    report.append("")
    report.append("-" * 60)
    report.append(heading)
    report.append("-" * 60)


def format_report(data, url):
    """Turn the extracted data into a human-readable report (list of lines)."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = []
    report.append("=" * 60)
    report.append("SCRAPING REPORT")
    report.append(f"URL:      {url}")
    report.append(f"Scraped:  {now}")
    report.append("=" * 60)

    section(report, "PAGE TITLE")
    report.append(data["title"])

    section(report, "META DESCRIPTION")
    report.append(data["description"])

    section(report, "META KEYWORDS")
    report.append(data["keywords"])

    section(report, "HEADINGS")
    for level in ("h1", "h2", "h3"):
        items = data["headings"][level]
        report.append(f"\n[{level.upper()}] ({len(items)} found)")
        if items:
            report.extend(f"  - {item}" for item in items[:MAX_LISTED_ITEMS])
            if len(items) > MAX_LISTED_ITEMS:
                report.append(f"  ... and {len(items) - MAX_LISTED_ITEMS} more")
        else:
            report.append("  (none)")

    links = data["links"]
    section(report, f"LINKS ({len(links)} unique)")
    if links:
        report.extend(f"  {i}. {link}" for i, link in enumerate(links[:MAX_LISTED_ITEMS], 1))
        if len(links) > MAX_LISTED_ITEMS:
            report.append(f"  ... and {len(links) - MAX_LISTED_ITEMS} more")
    else:
        report.append("  (none)")

    images = data["images"]
    section(report, f"IMAGES ({len(images)} found)")
    if images:
        report.extend(f"  {i}. {img}" for i, img in enumerate(images[:MAX_LISTED_ITEMS], 1))
        if len(images) > MAX_LISTED_ITEMS:
            report.append(f"  ... and {len(images) - MAX_LISTED_ITEMS} more")
    else:
        report.append("  (none)")

    text = data["text"]
    section(report, "VISIBLE TEXT")
    if text:
        report.append(text)
    else:
        report.append("  (no visible text found)")

    report.append("")
    report.append("=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)
    return "\n".join(report)


def ask_save_to_file(report):
    """Ask whether to save the report and, if yes, where."""
    answer = input("\nSave the output to a text file? (y/n): ").strip().lower()
    if answer not in ("y", "yes"):
        print("Okay, exiting without saving. Goodbye!")
        return

    while True:
        path = input("Enter the path of the output file (e.g. output/report.txt): ").strip()
        if not path:
            print("[!] Path cannot be empty. Try again or answer 'n' to quit.")
            answer = input("Save the output to a text file? (y/n): ").strip().lower()
            if answer not in ("y", "yes"):
                print("Okay, exiting without saving. Goodbye!")
                return
            continue

        directory = os.path.dirname(os.path.abspath(path))
        try:
            os.makedirs(directory, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(report + "\n")
            print(f"[+] Report saved successfully to: {os.path.abspath(path)}")
            break
        except PermissionError:
            print("[!] Permission denied for that location. Choose another path.")
        except OSError as exc:
            print(f"[!] Could not write to that path: {exc}")


def main():
    """Run the full scrape -> display -> optional save workflow."""
    print_banner()
    url = ask_for_url()

    print(f"\n[*] Fetching {url} ...")
    html = fetch_page(url)
    if html is None:
        print("[!] Unable to continue. Exiting.")
        sys.exit(1)

    print("[*] Parsing page content ...")
    soup, base_url = build_soup(html, url)
    data = extract_data(soup, base_url)

    print("[*] Generating report ...\n")
    report = format_report(data, url)
    print(report)

    ask_save_to_file(report)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Interrupted by user. Goodbye!")
        sys.exit(130)
