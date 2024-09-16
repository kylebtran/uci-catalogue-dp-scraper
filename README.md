# UCI Catalogue Degree Plan Scraper

## Overview

This tool is designed to scrape degree plans from the [UCI Catalogue](https://catalogue.uci.edu) by extracting degree plan tables, including course sequences and links to specific course information, from the university’s catalogue. The data is used to assist the **UCI Curricular Analytics** project. 

On a high level, it:

- Navigates to specific degree program pages.
- Extracts the degree plan tables, including the course sequences for different years.
- Captures hyperlinks associated with each course.
- Processes normal course listings and dynamically loaded content.

The scraper makes use of **Python**, primarily leveraging:

- `requests`: To fetch the HTML content from UCI's Catalogue.
- `BeautifulSoup`: To parse and extract the degree plan tables.
- `pandas`: To store the scraped data in a structured format (DataFrame) for further analysis or export.

## Procedure

1. Load URLs of UCI degree plans into `urls.txt` from the [UCI Catalogue](https://catalogue.uci.edu).
2. Run `script.py` and monitor progress through the console.
3. View scraped degree plans under the `sample_dp_exports/` directory.
