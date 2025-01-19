from typing import Optional
import requests
from bs4 import BeautifulSoup
from scraping_tool.storage.base_storage import BaseStorage
from scraping_tool.notifier.base_notifier import BaseNotifier
from scraping_tool.utils.caching import CacheManager
from scraping_tool.utils.retry import retry_request
import os
import time

class Scraper:
    def __init__(self, storage: BaseStorage, notifier: BaseNotifier, cache_manager: CacheManager):
        self.storage = storage
        self.notifier = notifier
        self.cache_manager = cache_manager

    def scrape(self, url: str, pages_limit: Optional[int] = None, proxy: Optional[str] = None):
        scraped_data = []
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        page = 1

        while True:
            if pages_limit and page > pages_limit:
                break

            current_url = f"{url}/page/{page}/"
            response = retry_request(lambda: requests.get(current_url, headers=headers, proxies=proxies))
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.select(".product-inner")

            if not products:
                break

            for product in products:
                title_tag = product.select_one(".woo-loop-product__title a")
                image_tag = product.select_one(".mf-product-thumbnail img")

                if title_tag and image_tag:
                    title = title_tag.text.strip()
                    image_url = image_tag.get("data-lazy-src") or image_tag.get("src")
                    if not image_url:
                        image_url = "https://example.com/default-image.jpg"

                    price_tag = product.select_one(".mf-product-price-box .price ins span")
                    if not price_tag:
                        price_tag = product.select_one(".mf-product-price-box .woocommerce-Price-amount")

                    if price_tag:
                        price = float(price_tag.text.strip().replace("₹", "").replace(",", ""))

                        cached_price = self.cache_manager.get_cache(title)
                        if cached_price is not None and cached_price == price:
                            print(f"Skipping cached product: {title} (Price unchanged: ₹{price})")
                            continue  
                        
                        image_path = self.download_image(image_url, title)

                        scraped_data.append({
                            "product_title": title,
                            "product_price": price,
                            "path_to_image": image_path,
                        })

                        self.cache_manager.set_cache(title, price)

            page += 1
        self.storage.save(scraped_data)
        self.notifier.notify(f"Scraped {len(scraped_data)} products.")
        return {"scraped_count": len(scraped_data)}

    def download_image(self, url: str, title: str):
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # Raise an error for non-2xx responses
            
            images_dir = os.path.abspath("images")
            os.makedirs(images_dir, exist_ok=True)
            
            timestamp = int(time.time() * 1000)
            sanitized_title = title.replace(' ', '_').replace('/', '_')  
            file_name = os.path.join(images_dir, f"{sanitized_title}_{timestamp}.jpg")
            
            with open(file_name, "wb") as img_file:
                img_file.write(response.content)
            
            print(f"Image downloaded: {file_name}")
            return file_name
        
        except requests.RequestException as e:
            print(f"Error downloading image for {title}: {e}")
        
        return os.path.join(images_dir, "default.jpg")
