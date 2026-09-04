import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

page = requests.get(url)
html = page.text

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", id="totals_stats")

# Read column names from the header row.
column_names = []
for header_cell in table.find("thead").find_all("th"):
    name = header_cell.get_text(strip=True)
    column_names.append(name)

# Read each body row into a list of cell values.
data_rows = []
for row in table.find("tbody").find_all("tr"):
    cells = []
    for cell in row.find_all(["th", "td"]):
        text = cell.get_text(strip=True)
        cells.append(text)

    if len(cells) == 0:
        continue

    # This table repeats the header (Rk, Player, ...) every so often. Skip those.
    if cells[0] == "Rk":
        continue

    data_rows.append(cells)

df = pd.DataFrame(data_rows, columns=column_names)
df = df.dropna()
print(df.head())

#   Rk                   Player Age Team Pos   G  GS    MP   FG  ...  TRB  AST  STL BLK  TOV   PF   PTS Trp-Dbl                        Awards
# 0  1              Luka Dončić  24  DAL  PG  70  70  2624  804  ...  647  686   99  38  282  149  2370      21          MVP-3,CPOY-6,AS,NBA1
# 1  2  Shai Gilgeous-Alexander  25  OKC  PG  75  75  2553  796  ...  415  465  150  67  162  184  2254       0   MVP-2,DPOY-7,CPOY-3,AS,NBA1
# 2  3    Giannis Antetokounmpo  29  MIL  PF  73  73  2567  837  ...  841  476   87  79  250  210  2222      10  MVP-4,DPOY-9,CPOY-12,AS,NBA1
# 3  4            Jalen Brunson  27  NYK  PG  77  77  2726  790  ...  278  519   70  13  186  144  2212       0          MVP-5,CPOY-5,AS,NBA2
# 4  5             Nikola Jokić  28  DEN   C  79  79  2737  822  ...  976  708  108  68  237  194  2085      25          MVP-1,CPOY-4,AS,NBA1
#
# [5 rows x 32 columns]

# Data Description:
#
# This data could be used for several purposes such as:
#
# - comparing the average age of the top players in the NBA and the average age of an MVP candidate
# - comparing the average offensive stats depending on position, for example how many more points PG score on average compared to centers
# - comparing the average triple doubles among top NBA players, and how that correlates with MVP awards and total points


