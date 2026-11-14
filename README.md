# Web Scraper 🕸️

A simple, interactive **command-line web scraper** written in Python, built on top of the popular **BeautifulSoup4** library together with **requests**.

The program asks you for the URL of a website, fetches the page, extracts the most useful information from it, prints a nicely formatted report straight to your terminal, and finally gives you the option to save that report to a plain-text file of your choosing.

---

## 📋 Table of Contents

1. [About This Project](#-about-this-project)
2. [Features](#-features)
3. [How It Works](#-how-it-works)
4. [Requirements](#-requirements)
5. [Installation](#-installation)
6. [Usage](#-usage)
7. [Example Session](#-example-session)
8. [What Gets Scraped](#-what-gets-scraped)
9. [Saving Output to a File](#-saving-output-to-a-file)
10. [Project Structure](#-project-structure)
11. [Error Handling](#-error-handling)
12. [Troubleshooting](#-troubleshooting)
13. [Legal & Ethical Notes](#-legal--ethical-notes)
14. [Limitations & Ideas for Improvement](#-limitations--ideas-for-improvement)
15. [Contributing](#-contributing)
16. [License](#-license)

---

## 🔍 About This Project

Web scraping is the process of automatically downloading a web page and extracting structured information from its HTML. This project is a small but complete, ready-to-run example of that process.

It was written with two goals in mind:

- **To be genuinely useful.** Point it at any public web page and you instantly get a clean, readable report containing the page title, meta description, headings, all unique links, all images, and the visible text content — with no clutter from scripts, styles, or advertisements baked into the HTML.
- **To be easy to read and learn from.** The entire scraper lives in a single Python file (`scraper.py`) of roughly 250 lines, organized into small, single-purpose functions. If you are learning BeautifulSoup4 or how scraping works in general, this file can serve as a practical reference.

There is **no configuration file, no command-line flags, and no complex setup** — just run it and answer the prompts.

---

## ✨ Features

- **Interactive workflow** — the program guides you step by step:
  1. Ask for the URL of the website to scrape.
  2. Fetch and parse the page.
  3. Display a formatted report in the terminal.
  4. Ask whether to save the output (`y/n`).
  5. If **y**, ask for the file path and write the report there.
  6. If **n**, quit cleanly.
- **Automatic URL normalization** — typing `example.com` works just as well as `https://example.com`.
- **Robust input validation** — empty or malformed URLs are rejected with a helpful message and re-prompted, so the program never crashes because of a typo.
- **Comprehensive extraction** — page title, meta description, meta keywords, all `h1`/`h2`/`h3` headings, every unique absolute link, every image, and the full visible text.
- **Relative link resolution** — links like `/about` or `../blog/post.html` are converted to full absolute URLs using the page's base URL (including `<base href>` tags when present).
- **Noise removal** — `<script>`, `<style>`, `<noscript>`, `<template>`, and `<svg>` elements are stripped before extracting text, so the output contains only what a human would actually see.
- **Truncated listings for huge pages** — links, images, and headings are capped at 50 entries each in the report (with a "... and N more" note) so the terminal output stays readable.
- **Graceful error handling** — connection failures, timeouts, HTTP errors (404, 500, etc.), invalid URLs, permission errors when writing files, and even `Ctrl+C` are all handled with clear messages instead of ugly tracebacks.
- **Zero configuration** — no arguments, no config files, no environment variables.

---

## ⚙️ How It Works

Under the hood, the scraper performs four distinct phases:

### 1. Fetching

The [`requests`](https://requests.readthedocs.io/) library performs an HTTP `GET` request against the URL you provide, sending a realistic browser `User-Agent` header so that most websites do not reject the request as bot traffic. The request times out after 15 seconds so the program never hangs forever on an unresponsive server.

### 2. Parsing

The downloaded HTML is handed to **BeautifulSoup4**, which builds a parse tree of the document. From this tree the scraper walks the DOM to pull out titles, metadata, headings, anchors, and image tags.

### 3. Extraction & formatting

All extracted pieces are collected into a data dictionary, then rendered into a human-readable, sectioned text report. Relative URLs are resolved to absolute ones with `urllib.parse.urljoin`, and duplicates are removed.

### 4. Display & optional save

The report is printed to the terminal in full. You are then asked whether to save it. If you answer `y`, you are prompted for a file path; parent directories are created automatically if they do not exist, and the report is written as UTF-8 text.

---

## 📦 Requirements

- **Python 3.7 or newer** (tested with 3.7 – 3.12)
- **Internet access** (obviously — the whole point is fetching web pages)
- The two third-party libraries below:

| Library | Purpose | PyPI Page |
|---|---|---|
| `requests` | Performs the HTTP request to download the page | [pypi.org/project/requests](https://pypi.org/project/requests/) |
| `beautifulsoup4` | Parses the HTML and lets us query the DOM | [pypi.org/project/beautifulsoup4](https://pypi.org/project/beautifulsoup4/) |

---

## 💽 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ryzoru1/Web_Scraper.git
cd Web_Scraper
```

### 2. (Recommended) Create a virtual environment

```bash
# On Linux / macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

That's it — the scraper is a single script with no other setup required.

---

## 🚀 Usage

Run the script from the project directory:

```bash
python scraper.py
```

The program will then interact with you through a series of prompts:

1. **`Enter the URL of the website to scrape:`** — type any website URL. A scheme is optional; `example.com` is automatically turned into `https://example.com`.
2. The page is fetched, parsed, and the **full report is printed** to your terminal.
3. **`Save the output to a text file? (y/n):`**
   - Answer **`y`** (or `yes`) → you will be prompted: `Enter the path of the output file (e.g. output/report.txt):` and the report is written to that path. Missing parent directories are created automatically.
   - Answer **`n`** (or anything else) → the program prints a goodbye message and exits without saving anything.

To stop the program at any moment, press `Ctrl+C` — it exits cleanly with a friendly message.

---

## 🖥️ Example Session

```
============================================================
              Python Web Scraper (BeautifulSoup4)
============================================================

Enter the URL of the website to scrape: example.com

[*] Fetching https://example.com ...
[*] Parsing page content ...
[*] Generating report ...

============================================================
SCRAPING REPORT
URL:      https://example.com
Scraped:  2024-11-14 12:00:00
============================================================

------------------------------------------------------------
PAGE TITLE
------------------------------------------------------------
Example Domain

------------------------------------------------------------
META DESCRIPTION
------------------------------------------------------------
(none)

------------------------------------------------------------
HEADINGS

[H1] (1 found)
  - Example Domain

------------------------------------------------------------
LINKS (1 unique)
  1. https://www.iana.org/domains/example

------------------------------------------------------------
VISIBLE TEXT
------------------------------------------------------------
Example Domain
This domain is for use in illustrative examples in documents.
...

============================================================
END OF REPORT
============================================================

Save the output to a text file? (y/n): y
Enter the path of the output file (e.g. output/report.txt): reports/example.txt
[+] Report saved successfully to: /home/user/Web_Scraper/reports/example.txt
```

---

## 🧺 What Gets Scraped

For every page, the report contains these sections:

| Section | Source in HTML | Notes |
|---|---|---|
| **Page Title** | `<title>` | Whitespace-trimmed text. |
| **Meta Description** | `<meta name="description">` | Shows `(none)` if the page has no description. |
| **Meta Keywords** | `<meta name="keywords">` | Shows `(none)` if absent. |
| **Headings** | `<h1>`, `<h2>`, `<h3>` | Grouped by level with counts; capped at 50 each. |
| **Links** | `<a href="...">` | Deduplicated, resolved to absolute URLs, HTTP/HTTPS only. |
| **Images** | `<img src="...">` | Deduplicated, resolved to absolute URLs. |
| **Visible Text** | Full document text | After removing `script`, `style`, `noscript`, `template`, and `svg` elements; blank lines removed. |

---

## 💾 Saving Output to a File

When you choose to save:

- You may give **any relative or absolute path**, e.g. `report.txt`, `output/example.txt`, or `/tmp/scrapes/example.txt`.
- If the **parent directory does not exist**, it is created for you.
- The file is written in **UTF-8**, so pages in any language are saved correctly.
- If the path is not writable (permissions, invalid characters, read-only filesystem), you get a clear error and are asked to choose a different path instead of the program crashing.
- The saved file contains exactly the same report you saw in the terminal, plus a trailing newline.

---

## 📁 Project Structure

```
Web_Scraper/
├── scraper.py         # The complete scraper (single-file program)
├── requirements.txt   # Pinned dependencies (requests, beautifulsoup4)
├── README.md          # This documentation
├── .gitignore         # Ignores caches, virtual envs, output files, etc.
└── LICENSE            # GNU General Public License v3.0
```

---

## 🛡️ Error Handling

The scraper is defensive at every step:

| Situation | Behavior |
|---|---|
| Empty URL input | Re-prompts with a message. |
| URL without a scheme (`example.com`) | `https://` is added automatically. |
| Malformed URL (no dot in the domain) | Re-prompts with a message. |
| Unreachable host / no internet | Prints `[!] Connection failed...` and exits with status 1. |
| Server does not respond within 15 s | Prints a timeout message and exits. |
| HTTP errors (403, 404, 500, ...) | Prints the exact HTTP error and exits. |
| Page has no `<title>` | Report shows `(no title found)` instead of crashing. |
| Unwritable output path | Prints the OS error and asks for a different path. |
| `Ctrl+C` at any prompt | Prints `[!] Interrupted by user. Goodbye!` and exits with status 130. |

---

## 🩺 Troubleshooting

**`ModuleNotFoundError: No module named 'bs4'`**
You have not installed the dependencies. Run `pip install requests beautifulsoup4` (inside your virtual environment if you use one).

**`[!] HTTP error: 403 Client Error: Forbidden`**
The site is blocking non-browser requests. Some websites aggressively block scrapers regardless of the `User-Agent` header. Try a different site, or respect the site's wishes — see the legal notes below.

**`[!] Connection failed.`**
Check your internet connection and the spelling of the URL.

**The text section looks empty.**
Some pages render all of their content with client-side JavaScript. BeautifulSoup only sees the raw HTML returned by the server, so a JavaScript-only page appears empty. This is a known limitation of all `requests` + BeautifulSoup scrapers (see [Limitations](#-limitations--ideas-for-improvement)).

**Weird characters in the output.**
The report is UTF-8. If your terminal or text editor uses another encoding, switch it to UTF-8.

---

## ⚖️ Legal & Ethical Notes

Web scraping sits in a legal and ethical gray zone that depends heavily on **what** you scrape, **how** you scrape it, and **what you do with the data**. As the user of this tool, you are responsible for using it lawfully. A few guidelines:

- **Check `robots.txt`.** Most websites publish their scraping policy at `https://<site>/robots.txt`. Respect it.
- **Read the Terms of Service.** Many sites explicitly forbid automated access.
- **Do not hammer servers.** This tool fetches a single page per run, which is harmless — but do not wrap it in a loop that floods a website with requests.
- **Do not scrape personal data.** Collecting names, emails, or other personal information without consent may violate privacy laws such as the GDPR.
- **Respect copyright.** The text you scrape usually belongs to someone else.
- **Do not bypass authentication or paywalls.** This tool only performs plain, unauthenticated GET requests — keep it that way.

This software is provided for **educational purposes**. The author is not responsible for misuse.

---

## 🚧 Limitations & Ideas for Improvement

Known limitations of the current version:

- **No JavaScript rendering.** Pages that build their content in the browser with JavaScript will appear mostly empty. Integrating something like `playwright` or `selenium` would fix this, at the cost of a much heavier dependency.
- **Single page per run.** The scraper does not crawl; it fetches exactly one URL per invocation.
- **No CSS selectors for custom extraction.** You cannot (yet) say "give me every element with class `product-price`".

Ideas that would make good first contributions:

- [ ] Add an optional CLI argument to skip the prompts: `python scraper.py https://example.com -o report.txt`
- [ ] Support saving as Markdown, JSON, or CSV in addition to plain text.
- [ ] Add a `--depth N` option for simple crawling of linked pages.
- [ ] Add polite rate limiting and `robots.txt` checking.
- [ ] Use `lxml` as the parser for a significant speed boost on large pages.
- [ ] Add a test suite with `pytest` and mocked HTTP responses.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request describing what you changed and why.

Please keep the code style consistent with the existing single-file layout and keep the program dependency-light.

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for the full text.

In short: you are free to use, modify, and distribute this software, but any derivative work must also be licensed under the GPL-3.0.
