"""
AIPI 510 - Week 2 Sync Activity (API)
file: caleb.py

This python file web scrapes data from OpenF1.org and parses the data into a pandas DataFrame.
"""

import requests
import pandas as pd
import json

def get_f1_locations(year):
    # 1. Create the API endpoint URL
    url = 'https://api.openf1.org/v1/sessions'

    # 2. Set query parameters
    params = {"year": year}

    # 3. Make the request
    response = requests.get(url, params=params)

    # 4. Test the request
    if response.status_code == 200:
        print("Good Response")
    else:
        print("Request failed. Error: ", response.status_code)

    # 4. Parse JSON
    data = response.json()

    f1_locations = []

    # 5. Create parsed dictionary from 'data'
    for session in data:
        location = session['location']
        country = session['country_name']
        date_start = session['date_start']
        date_end = session['date_end']

        f1_locations.append({
        "Location": location,
        "Country": country,
        "Start Date": date_start,
        "End Date": date_end
    })
    return f1_locations
    
year = input("Specify year to find locations of F1 sessions: ")
f1_locations = get_f1_locations(year)

df = pd.DataFrame(f1_locations).dropna(inplace=False)
print(df.head())

"""
This python file scrapes data from previous Formula 1 racing years and provides time periods and locations for
each racing session. This python file could be used to identify trends in where Formula 1 racing hosts races. 
The results could determine business planning for organizations that are looking to project where to
invest in the growth of the sport's fan base. It could also be used to build predictive models by event-based 
companies to predict where to surge resources over the next 5-10 year period.

"""