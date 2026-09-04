# Step 1: Import libraries
import requests
import json
import pandas as pd

# Step 2: Choose an API and read the documentation
# TheSportsDB is a regular public sports API (no API key).
# Docs: https://www.thesportsdb.com/api.php
url = "https://www.thesportsdb.com/api/v1/json/3/search_all_teams.php?l=NBA"

# Step 3: Makes a GET request
page = requests.get(url)

# Step 4: Parses the JSON response
# The JSON is a dict with a "teams" list. Each item is one team.
data = json.loads(page.text)
teams = data["teams"]

# Step 5: Stores relevant fields into a DataFrame
# Keep team name, abbreviation, city, stadium, and year founded.
df = pd.DataFrame(teams)
df = df[["strTeam", "strTeamShort", "strLocation", "strStadium", "intFormedYear"]]

# Step 6: Print the first 5 rows of your DataFrame
print(df.head().to_string())

#              strTeam strTeamShort                strLocation        strStadium intFormedYear
# 0      Atlanta Hawks          ATL           Atlanta, Georgia  State Farm Arena          1946
# 1     Boston Celtics          BOS      Boston, Massachusetts         TD Garden          1946
# 2      Brooklyn Nets          BKN         Brooklyn, New York   Barclays Center          1967
# 3  Charlotte Hornets          CHA  Charlotte, North Carolina   Spectrum Center          1988
# 4      Chicago Bulls          CHI          Chicago, Illinois     United Center          1966

# Step 7: Add 3–5 lines of notes at the bottom of the script describing the data and possible uses
#
# This data includes general sports team information such as name, location, and stadiums.
# This data can be used to populate web pages with overviews of various teams from different
# sports leagues, a catalog of professional sports.
#
# For example, a web page could be created that allows a user to sort by city and then output
# all different teams associated with that city e.g. Dallas Cowboys, Dallas Mavericks, Dallas
# Stars and then see where each stadium is. The site would be powered by pulling data from this API.
