from fastapi import FastAPI, Depends, HTTPException, status, Body
from scraper import Scraper
from database import DatabaseHandler
from notifier import Notifier
import os

app = FastAPI()

API_TOKEN = "abhjgnagoga"

def get_token_header(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    
@app.post("/scrape")
def scrape_data(token = Depends(get_token_header), request = Body(...)):
    scraper = Scraper(pages_limit=request["pages_limit"], proxy=request["proxy"], token=token)
    scraped_data = scraper.scrape()

    db_handler = DatabaseHandler()
    updated_count = db_handler.update_database(scraped_data)

    notifier = Notifier()
    notifier.notify(updated_count)

    return {"message": f"{updated_count} products scraped and updated."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))