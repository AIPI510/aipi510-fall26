import json
import requests
import pandas as pd

pokemon_params = ['pikachu', 'charizard', 'bulbasaur', 'squirtle','metapod','butterfree','pidgeotto','rattata','ekans','nidoqueen','ninetales','jigglypuff','zubat','oddish','diglett','meowth','psyduck','golduck','growlithe','poliwag','machop','machamp','arceus']

all_pokemons = []

 # PokeAPI takes the Pokémon name directly in the URL path (no query params needed)
for pokemons in pokemon_params:
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemons}")
    data = response.json()

    # Checking what features are available
    pokemon_dict = {}
    pokemon_name = data['name']
    pokemon_height_decimeters = data['height']
    pokemon_weight_hectograms = data['weight']
    pokemon_base_experience = data['base_experience']

    # Nested fields: "types" and "abilities" are lists of dicts, so have to traverse to extract type and ability names
    pokemon_type = data['types'][0]['type']['name']
    # Keeping only the first ability for simplicity, some pokemons might have multiple abilities but harder to store in cells
    pokemon_ability = data['abilities'][0]['ability']['name']

    pokemon_dict["name"] = pokemon_name
    pokemon_dict["type"] = pokemon_type
    pokemon_dict["height_in_decimeters"] = pokemon_height_decimeters
    pokemon_dict["hectograms"] = pokemon_weight_hectograms
    pokemon_dict["base_experience"] = pokemon_base_experience
    pokemon_dict["ability"] = pokemon_ability

    all_pokemons.append(pokemon_dict)


pokemon_df = pd.DataFrame(all_pokemons)

print(pokemon_df.head())


# --- Notes on this dataset ---
# This data comes from PokéAPI and covers 23 Pokémon spanning several types
# (electric, fire, grass, water, poison, etc.). Each row has the Pokémon's
# name, primary type, height (decimeters), weight (hectograms), base
# experience, and first listed ability.
# Note: height/weight are in PokéAPI's native units (decimeters/hectograms),
# not meters/kg. Also, some Pokémon have 2+ types or abilities — this only
# captures the first of each for simplicity.
# Could be used to compare stats across types, build a simple Pokémon
# lookup tool, or as practice data for classification models (e.g.
# predicting type from stats).


