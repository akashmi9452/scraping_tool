from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from scraping_tool.scraper import Scraper
from scraping_tool.storage.json_storage import JSONStorage
from scraping_tool.notifier.console_notifier import ConsoleNotifier
from scraping_tool.utils.caching import CacheManager
from scraping_tool.utils.auth import authenticate_request
from scraping_tool.utils.retry import retry_request
import os

app = FastAPI()

class ScraperSettings(BaseModel):
    pages_limit: Optional[int] = Field(None, description="Limit on the number of pages to scrape.")
    proxy: Optional[str] = Field(None, description="Proxy string for scraping.")

storage = JSONStorage(file_path="scraped_data.json")
notifier = ConsoleNotifier()
cache_manager = CacheManager(redis_host="localhost", redis_port=6379)
scraper = Scraper(storage=storage, notifier=notifier, cache_manager=cache_manager)

@app.get("/scrape", dependencies=[Depends(authenticate_request)])
def scrape_catalogue(settings: ScraperSettings):
    """
    Endpoint to scrape product information from a catalogue.
    
    Args:
        settings (ScraperSettings): Scraper settings including pages limit and proxy.
    
    Returns:
        dict: Scraping summary.
    """
    try:
        summary = scraper.scrape(
            url="https://dentalstall.com/shop/",
            pages_limit=settings.pages_limit,
            proxy=settings.proxy
        )
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
