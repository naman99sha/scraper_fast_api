import requests
from bs4 import BeautifulSoup
import os
import time

class Scraper:
    #constructor to initialize url and other information
    def __init__(self, pages_limit=5, proxy=None):
        self.base_url = "https://dentalstall.com/shop/"
        self.pages_limit = pages_limit
        self.proxy = proxy
        self.proxies = {"http": proxy, "https": proxy} if proxy else None

    #fetch page function
    def fetch_page(self, url):
        try:
            response = requests.get(url, proxies=self.proxies)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching {url} - {e}")
            return