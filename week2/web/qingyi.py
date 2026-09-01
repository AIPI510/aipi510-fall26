"""Scrape Luka Doncic's per-game stats from Basketball-Reference into a DataFrame."""

import io
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment

URL = "https://www.basketball-reference.com/players/d/doncilu01.html"
TABLE_IDS = ["per_game_stats", "per_game"]  # site has changed this id over time
OUTPUT = "doncic_per_game.csv"


def fetch(url: str) -> str:
    """Get the page HTML. BBRef returns 403 without a browser User-Agent."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def find_table(html: str, table_ids: list[str]):
    """Locate the target table, including tables hidden inside HTML comments."""
    soup = BeautifulSoup(html, "html.parser")

    for tid in table_ids:
        table = soup.find("table", id=tid)
        if table is not None:
            return table

    # BBRef wraps many secondary tables in <!-- --> to defer rendering
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if "<table" not in comment:
            continue
        sub = BeautifulSoup(comment, "html.parser")
        for tid in table_ids:
            table = sub.find("table", id=tid)
            if table is not None:
                return table

    found = [t.get("id") for t in soup.find_all("table")]
    raise ValueError(f"None of {table_ids} found. Table ids on page: {found}")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop repeated headers, summary rows, and empty rows; coerce numeric types."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[-1] for c in df.columns]
    df.columns = [str(c).strip() for c in df.columns]

    season_col = df.columns[0]

    # Drop rows that are entirely empty
    df = df.dropna(how="all")

    # Drop repeated header rows (the season cell literally reads "Season")
    df = df[df[season_col].astype(str).str.strip() != season_col]

    # Keep only real season rows (e.g. 2018-19); removes Career/team totals in tfoot
    df = df[df[season_col].astype(str).str.match(r"^\d{4}-\d{2}$", na=False)]

    # Convert anything numeric; leave text columns (Season, Team, Pos) alone
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.notna().sum() > 0:
            df[col] = converted

    # Drop rows missing the core counting stats
    core = [c for c in ("G", "MP", "PTS") if c in df.columns]
    if core:
        df = df.dropna(subset=core)

    return df.reset_index(drop=True)


def main() -> pd.DataFrame:
    html = fetch(URL)
    table = find_table(html, TABLE_IDS)
    df = pd.read_html(io.StringIO(str(table)))[0]
    df = clean(df)

    print(df.head(5))
    print(f"\nShape: {df.shape}")

    df.to_csv(OUTPUT, index=False)
    return df


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# NOTES ON THE DATA
#
# Each row is one NBA regular season for Luka Doncic (2018-19 onward), scraped
# from his Basketball-Reference per-game table. Columns cover games played and
# started, minutes, and per-game averages for shooting (FG/3P/2P/FT with
# attempts and percentages), rebounds, assists, steals, blocks, turnovers,
# fouls, and points.
#
# Note the values are already season averages, not raw totals, so rows are not
# additive — a career average has to be weighted by games played, not taken as
# a plain mean. Percentage columns are NaN in any season with zero attempts of
# that shot type, which is why the numeric coercion uses errors="coerce"
# rather than failing. Seasons split across two teams appear as multiple rows
# with a TOT/2TM aggregate row, so filter on team before aggregating.
#
# Useful for plotting a career trajectory (PTS/AST/TRB by season), checking
# whether efficiency improved as usage rose, or as one player's slice of a
# larger table built by looping the same scraper over many player URLs.
# ---------------------------------------------------------------------------
