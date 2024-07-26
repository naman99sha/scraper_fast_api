from fastapi import FastAPI, Depends, HTTPException, status
from scraper import Scraper
from pydantic import BaseModel
import os

app = FastAPI()

API_TOKEN = "abhjgnagoga"

def get_token_header(token):
    if str(token) != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
class ScrapeSettings(BaseModel):
    pages_limit: int = 5
    proxy: str = None
    
@app.post("/scrape", dependencies=[Depends(get_token_header)])
def scrape_data(settings: ScrapeSettings):
    scraper = Scraper(pages_limit=settings.pages_limit, proxy=settings.proxy)
    scraped_data = scraper.scrape()

    return {"message": f"successfully scraped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))