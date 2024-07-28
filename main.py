# main.py
from fastapi import FastAPI, HTTPException, Depends , Header
from pydantic import BaseModel
from typing import Optional
from functools import lru_cache
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

# Authentication token
API_TOKEN = "your_static_token"

   
def verify_token(token: str = Header(...)):
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

class ScrapeSettings(BaseModel):
    pages_limit: Optional[int] = None
    proxy: Optional[str] = None

# In-memory cache
cache = {}

def retry_request(url, headers, proxies, retries=3):
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Retry error for {url}: {e}")
    return None

def scrape_website(pages_limit: Optional[int], proxy: Optional[str]):
    base_url = "https://dentalstall.com/shop/"
    headers = {"User-Agent": "Mozilla/5.0"}
    proxies = {"http": proxy, "https": proxy} if proxy else None

    products = []

    for page in range(1, pages_limit + 1 if pages_limit else 10):
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}page/{page}/"
        
        response = retry_request(url, headers, proxies)
        if response is None:
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        product_cards = soup.find_all("li", class_="product")
        # print(product_cards)

        for card in product_cards:
            title_tag = card.find("h2", class_="woo-loop-product__title").find("a")
            title = title_tag.get_text(strip=True)
            img_tag = card.find("img", class_="attachment-woocommerce_thumbnail")
            img_url = img_tag["data-lazy-src"] if "data-lazy-src" in img_tag.attrs else img_tag["src"]
            price_tag = card.find("span", class_="woocommerce-Price-amount")
            price = price_tag.get_text(strip=True)
            price = float(price.replace("₹", "").replace(",", "").strip())

            product = {
                "product_title": title,
                "product_price": price,
                "path_to_image": img_url,
            }

            # Caching check
            if title in cache and cache[title]['product_price'] == price:
                continue

            cache[title] = product
            products.append(product)

    return products



def save_to_json(data, filename="products.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

@app.get("/")
def read_root():
    return {"message": "Welcome to the scraping API"}

@app.post("/scrape", dependencies=[Depends(verify_token)])
def scrape(settings: ScrapeSettings):
    products = scrape_website(settings.pages_limit, settings.proxy)

    # Save products to a JSON file
    save_to_json(products)

    # Notify scraping status
    print(f"Scraped {len(products)} products.")

    return {"scraped_products": len(products)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
