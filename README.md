# scraper_fast_api

Steps to run this project: 
 - Run command "pip install -r requirements.txt" to install all the required libraries for this repo
 - Run command "python main.py" to start the server
 - In postman or any other similar tool pass the following post request:
    -> url = localhost:8000/scrape
    -> authentication: Bearer token = abhjgnagoga
    -> body(optional) = {
                "pages_limit": 1,
                "proxy": null
            }
 - Adjust the body parameters according to your requirement. By default the page limit is set to 5 
