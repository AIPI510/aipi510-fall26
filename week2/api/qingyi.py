"""Fetch meals from TheMealDB into a DataFrame."""

import string
import time

import pandas as pd
import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1"
API_KEY = "1"


def fetch_meals_by_letter(letter: str) -> list[dict]:
    """search.php?f= returns full meal objects, not just thumbnails."""
    resp = requests.get(f"{BASE_URL}/search.php", params={"f": letter}, timeout=30)
    resp.raise_for_status()
    # the API returns {"meals": null} for letters with no matches
    return resp.json().get("meals") or []


def fetch_all() -> list[dict]:
    """Walk a-z. 26 requests, roughly 300 meals."""
    meals = []
    for letter in string.ascii_lowercase:
        batch = fetch_meals_by_letter(letter)
        meals.extend(batch)
        print(f"  {letter}: {len(batch)} meals")
        time.sleep(0.5)  # be polite to a free API
    return meals


def collapse_ingredients(meal: dict) -> tuple[str, int]:
    """Fold strIngredient1..20 / strMeasure1..20 into one string plus a count."""
    parts = []
    for i in range(1, 21):
        ingredient = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        if not ingredient:  # empty slots are "" or None, not absent
            continue
        parts.append(f"{measure} {ingredient}".strip())
    return "; ".join(parts), len(parts)


def to_dataframe(meals: list[dict]) -> pd.DataFrame:
    rows = []
    for meal in meals:
        ingredients, n_ingredients = collapse_ingredients(meal)
        instructions = (meal.get("strInstructions") or "").strip()
        rows.append({
            "meal_id": meal.get("idMeal"),
            "name": meal.get("strMeal"),
            "category": meal.get("strCategory"),
            "area": meal.get("strArea"),
            "tags": meal.get("strTags"),
            "n_ingredients": n_ingredients,
            "ingredients": ingredients,
            "instruction_chars": len(instructions),
            "has_video": bool(meal.get("strYoutube")),
            "thumbnail": meal.get("strMealThumb"),
        })
    return pd.DataFrame(rows)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop unusable rows, normalise blanks, fix dtypes."""
    df = df.dropna(subset=["meal_id", "name"])
    df = df.drop_duplicates(subset="meal_id")

    df["meal_id"] = pd.to_numeric(df["meal_id"], errors="coerce").astype("Int64")

    # the API uses "" and whitespace for missing text, not null
    for col in ["name", "category", "area", "tags"]:
        df[col] = df[col].astype("string").str.strip().replace("", pd.NA)

    # a meal with no ingredients parsed is not usable
    df = df[df["n_ingredients"] > 0]

    return df.sort_values("meal_id").reset_index(drop=True)


def main() -> pd.DataFrame:
    print("Fetching meals a-z...")
    df = clean(to_dataframe(fetch_all()))

    print("\n", df.head(5).to_string(), sep="")
    print(f"\nShape: {df.shape}")
    print(f"Categories: {df['category'].nunique()}, Areas: {df['area'].nunique()}")
    return df


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# NOTES ON THE DATA
#
# Each row is one recipe from TheMealDB, a community-maintained recipe
# database, fetched through its free JSON API. Columns cover the dish name, its
# category (Beef, Vegetarian, Dessert...), its cuisine of origin, free-text
# tags, the ingredient list, how many ingredients it uses, how long the written
# instructions are, and whether a video walkthrough exists.
#
# Useful for exploring how ingredient count varies by cuisine, for building a
# simple content-based recipe recommender on the ingredient text, or as a
# starting corpus for ingredient-name normalisation, since the same item shows
# up with inconsistent spelling and casing across recipes.
# ---------------------------------------------------------------------------