import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get HTML content from Basketball Reference
BBREF_URL = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"
response = requests.get(BBREF_URL)

# Let the Requests library make a prediction about the encoding used on the 
# webpage to avoid "nonsense" characters
response.encoding = response.apparent_encoding

# Parse raw HTML into human readable text and select the table of interest
soup = BeautifulSoup(response.text, 'html.parser')
player_stats_table_html = soup.find(id='totals_stats')
rows = player_stats_table_html.find_all("tr")

# Populate dataframe columns with table headings
header = rows.pop(0)
df_columns = [col['aria-label'].lower() for col in header.find_all("th")]

# Populate dataframe rows with table data. Remove empty string artifacts from 
# HTML.
records = []
for row in rows:
    records.append(
        [child.text for child in row.children if child.text.strip()]
    )

# Construct dataframe
df = pd.DataFrame(records, columns=df_columns)

# Remove duplicate player rows related to multiple stat accumulations with 
# distinct teams
df.drop_duplicates(subset=["player"], inplace=True)
df.reset_index(drop=True, inplace=True)

# Display the first five entries of dataframe
print(df.head(100).to_string())

# ============================================================================
# The data in this dataframe includes player biographical information and 
# describes performance in sereral key statistics. Columns correspond to 
# individual biographical fields (name, position, team, age), statistical 
# categories (points, rebounds, shooting percentages, etc.), and award 
# finishes; row entries correspond to players. Row entries are ordered by 
# points scored. In addition to using the data contained in the dataframe for 
# producing descriptive statistics for individual players or composite 
# profiles** (like teams, divisions, conferences), two obvious modeling 
# opportunities jump out to me based on this dataset alone. The first involves 
# using statistical performance to predict award finishes. An idealized verison 
# of this model would likely be trained multiple seasons worth of data so that
# the model does not overfit to the type(s) of players who ranked highly in 
# award rankings for a given year -- although it would also likely be weighted
# towards recent years to reflect modern voter preferences. Another model would 
# work in the opposite direction, using age to predict statistical decline.