from fastapi import FastAPI, Depends, HTTPException, status
from scraper import Scraper
import os

app = FastAPI()

API_TOKEN = "abhjgnagoga"

def get_token_header(token):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
@app.post("/scrape", dependencies=[Depends(get_token_header)])
def scrape_data():
    scraper = Scraper()
    scraped_data = scraper.scrape()

    return {"message": f"successfully scraped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))