from pydantic import BaseModel, Field
from typing import Optional

class ScrapeSettings(BaseModel):
    max_pages: Optional[int] = Field(default=None, description="Number of pages to scrape")
    proxy: Optional[str] = Field(default=None, description="Proxy string to use for scraping")
