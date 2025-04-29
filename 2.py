# File: scraper/psu_jobs_btech_noexp.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re

BASE_URL = "https://govtjobguru.in/govt-jobs-by-department/govt-jobs-in-psu/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def parse_jobs(soup: BeautifulSoup) -> list:
    jobs_data = []
    job_cards = soup.select(".entry-content table tr")
    degree_pattern = re.compile(r"\b(btech|b\.tech|engineering degree)\b", re.IGNORECASE)

    for card in job_cards[1:]:
        cols = card.find_all("td")
        if len(cols) < 5:
            continue
        title = cols[0].get_text(strip=True)
        org = cols[1].get_text(strip=True)
        qualification = cols[2].get_text(strip=True)
        experience = cols[3].get_text(strip=True)
        last_date = cols[4].get_text(strip=True)

        if degree_pattern.search(qualification):
            link_tag = cols[0].find("a")
            job_link = urljoin(BASE_URL, link_tag['href']) if link_tag else ""
            jobs_data.append({
                "Job Title": title,
                "Organization": org,
                "Qualification": qualification,
                "Experience": experience,
                "Last Date": last_date,
                "Job Link": job_link
            })
    return jobs_data

def save_to_csv(jobs: list, filename: str = "btech_jobs.csv") -> None:
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)

def main():
    soup = fetch_page(BASE_URL)
    jobs = parse_jobs(soup)
    if jobs:
        save_to_csv(jobs)
        print(f"Saved {len(jobs)} jobs to btech_jobs.csv")
    else:
        print("No matching jobs found.")

if __name__ == "__main__":
    main()
