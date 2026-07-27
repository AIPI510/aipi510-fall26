# STATION 1: Web Scraping

## Objective:
Scrape tabular data from a webpage using requests and BeautifulSoup (or optionally pandas.read_html).
###Example Targets:
- https://www.basketball-reference.com/leagues/NBA_2024_totals.html
- https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)


## Step-by-step:
1. Clone the class repo and branch off of the branch week2-sourcedata (only do once, at your first station) 
2. Create a new branch yourname-week2 (only do once, at your first station)
3. Create a new file named yourname.py in scrape/ 
4. Import the libraries:
```
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

5. Use requests.get(url) to download HTML from your selected page.
6. Use BeautifulSoup to find the desired <table> and parse it into a DataFrame.
7. Clean the data (e.g., drop rows with missing values or headers repeated in the table).
8. Print the first 5 rows.
9. Add 3–5 lines of notes at the bottom of the script describing your data and how you might use it.
10. Commit
