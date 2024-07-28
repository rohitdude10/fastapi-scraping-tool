# FastAPI Scraping Tool

## Overview

This FastAPI application scrapes product information from the [Dental Stall](https://dentalstall.com/shop/) website. The tool fetches the product name, price, and image, and stores the scraped data in a local JSON file. It supports limiting the number of pages to scrape, using a proxy, and provides simple authentication.

## Features

- Scrape product name, price, and image from the catalog.
- Limit the number of pages to scrape.
- Use a proxy for scraping.
- Store scraped data in a local JSON file.
- Notify the number of products scraped.
- Simple token-based authentication.
- In-memory caching to avoid redundant updates.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/rohitdude10/fastapi-scraping-tool.git
    cd fastapi-scraping-tool
    ```

2. **Install required packages**:
    ```bash
    pip install fastapi uvicorn requests beautifulsoup4
    ```

## Running the Application

Start the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload


Scrape Endpoint
URL: /scrape
Method: POST
Description: Scrapes product information from the specified number of pages and stores the data in a local JSON file. It requires a valid token for authentication.
Request Headers
token: The static token for authentication (e.g., your_static_token).
Request Body
pages_limit (optional): The number of pages to scrape (e.g., 5).
proxy (optional): The proxy URL to use for scraping (e.g., http://your-proxy-url).

curl -X POST "http://127.0.0.1:8000/scrape" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-H "token: your_static_token" \
-d '{"pages_limit": 5, "proxy": "http://your-proxy-url"}'


import requests

url = "http://127.0.0.1:8000/scrape"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "token": "your_static_token"
}
data = {
    "pages_limit": 5,
    "proxy": "http://your-proxy-url"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())

response:

{
    "scraped_products": 20
}
