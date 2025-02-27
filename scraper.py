import requests
from bs4 import BeautifulSoup
import os
import time

class Scraper:
    #constructor to initialize url and other information
    def __init__(self, pages_limit=5, proxy=None, max_retries=3, retry_delays=5, token="abhjgnagoga"):
        self.base_url = "https://dentalstall.com/shop/"
        self.pages_limit = pages_limit
        self.proxy = proxy
        self.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.max_retries = max_retries
        self.retry_delays = retry_delays
        self.token = token

    #fetch page function
    def fetch_page(self, url):
        for attempt in range(self.max_retries):
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = requests.get(url, proxies=self.proxies, headers=headers)
                response.raise_for_status()
                return response.content
            except Exception as e:
                print(f"Error while fetching {url} - {e}")
                if attempt < self.max_retries-1:
                    print(f"Retrying in {self.retry_delays} seconds...")
                    time.sleep(self.retry_delays)
                else:
                    print(f"Failed to fetch {url} after {self.max_retries} attempts.")
                    return None
    
    def scrape(self):
        products = []
        for page in range(1, self.pages_limit+1):
            if page == 1:
                url = f"{self.base_url}/"
            else:
                url = f"{self.base_url}page/{page}/"
            content = self.fetch_page(url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                for product_card in soup.select("li.product"):
                    title_tag = product_card.select_one(".woo-loop-product__title a")
                    title = title_tag["href"]
                    product_name = title.split("/")[-2].replace("-"," ")

                    price_tag = product_card.select_one(".price ins .woocommerce-Price-amount")
                    if price_tag:
                        price = price_tag.get_text(strip=True).replace("₹", "")
                    else:
                        price_tag = product_card.select_one(".price .woocommerce-Price-amount")
                        price = price_tag.get_text(strip=True).replace("₹", "")

                    image_tag = product_card.select_one("img.attachment-woocommerce_thumbnail")
                    image_url = image_tag.get("data-lazy-src", image_tag.get("src"))

                    image_path = self.download_image(image_url, product_name, page)
                    
                    products.append({
                        "product_title": product_name,
                        "product_price": float(price.replace(",", "")),  # Handle comma in price if any
                        "path_to_image": image_path
                    })
        return products

    def download_image(self, url, title, page):
        response = requests.get(url, stream=True)
        image_path = f"images/page_{page}/{title.replace('/', '_').replace(' ', '_')}.jpg"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb') as out_file:
            out_file.write(response.content)
        return image_path                

# <h2 class="woo-loop-product__title"><a href="https://dentalstall.com/product/3m-espe-sof-lex-finishing-strips-refills/">3m Espe Sof-Lex Finishing Str...</a></h2>
# <img loading="lazy" width="300" height="300" src="https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-300x300.jpg" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail entered lazyloaded" alt="3m Espe Sof-Lex Finishing Strips - Refills - Dentalstall India" decoding="async" data-lazy-srcset="https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-300x300.jpg 300w, https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-100x100.jpg 100w, https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-150x150.jpg 150w, https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill.jpg 600w" data-lazy-sizes="(max-width: 300px) 100vw, 300px" title="3m Espe Sof-Lex Finishing Strips - Refills - Dentalstall India" data-lazy-src="https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-300x300.jpg" data-ll-status="loaded" sizes="(max-width: 300px) 100vw, 300px" srcset="https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-300x300.jpg 300w, https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-100x100.jpg 100w, https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill-150x150.jpg 150w, https://dentalstall.com/wp-content/uploads/2023/03/3m_espe_sof-lex_finishing_strips_-_refill.jpg 600w">

# <span class="woocommerce-Price-amount amount"><bdi><span class="woocommerce-Price-currencySymbol">₹</span>5395.00</bdi></span>