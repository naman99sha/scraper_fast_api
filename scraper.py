import requests
from bs4 import BeautifulSoup
import os
import time

class Scraper:
    #constructor to initialize url and other information
    def __init__(self, pages_limit=5, proxy=None, max_retries=3, retry_delays=5):
        self.base_url = "https://dentalstall.com/shop/"
        self.pages_limit = pages_limit
        self.proxy = proxy
        self.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.max_retries = max_retries
        self.retry_delays = retry_delays

    #fetch page function
    def fetch_page(self, url):
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, proxies=self.proxies)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Error while fetching {url} - {e}")
                if attempt < self.max_retries-1:
                    print(f"Retrying in {self.retry_delays} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"Failed to fetch {url} after {self.max_retries} attempts.")
                    return None