# UCI Catalogue Degree Plan Scraper

## Overview

This tool is designed to scrape degree plans from the [UCI Catalogue](https://catalogue.uci.edu) and automates the process of extracting degree plan tables, including course sequences and links to specific course information, from the university’s catalogue. The scraped data is used to assist in curricular analytics, with a specific focus on integrating it with the **UCI Curricular Analytics** project.

## How It Works

This tool web scrapes pages from the UCI Catalogue, focusing on the degree plan tables for undergraduate programs. It:

- Navigates to specific degree program pages.
- Locates and extracts the degree plan tables, including the course sequences for different years (Freshman through Senior).
- Captures hyperlinks associated with each course for further information retrieval.
- Processes both normal course listings and dynamically loaded content (like tooltips or pop-ups with additional course details).

The scraper makes use of **Python**, primarily leveraging:

- `requests`: To fetch the HTML content from UCI's Catalogue.
- `BeautifulSoup`: To parse and extract the degree plan tables.
- `pandas`: To store the scraped data in a structured format (DataFrame) for further analysis or export.
