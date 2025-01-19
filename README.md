# Scraping Tool

This repository contains a Python-based web scraping tool built using `FastAPI`, `BeautifulSoup`, and `Redis`. It allows you to scrape data from e-commerce websites and store it efficiently.

## Features
- Scrapes product details and images from websites.
- Utilizes caching to avoid redundant processing.
- FastAPI-based API for easy interaction.
- Support for proxy configuration.

## Requirements
- Python 3.9+
- Redis

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/akashmi9452/scraping-tool.git
   cd scraping-tool
2. Create and activate a Python virtual environment:
    python3 -m venv scraping-env
    source scraping-env/bin/activate
3. Install the dependencies:
    pip install fastapi uvicorn requests beautifulsoup4 redis
4. Start Redis (macOS example):
    brew services start redis

## Running the API

1. Start the FastAPI server:
    uvicorn main:app --reload
2. The API will be available at http://127.0.0.1:8000.

## Endpoints

1. Scrape Data
    Endpoint: /scrape
    Method: POST
    Description: Initiates a scraping operation.
    Request Body: {
        "url": "https://example.com/shop",
        "pages_limit": 5,
        "proxy": "http://yourproxy.com:port"
        }
    Example curl Command:
        curl -X POST "http://127.0.0.1:8000/scrape" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://dentalstall.com/shop", "pages_limit": 5}'

