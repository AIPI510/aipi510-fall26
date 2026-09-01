import requests
import pandas as pd

url = (
    "https://www.speedrun.com/api/v1/leaderboards/"
    "j1npme6p/category/mkeyl926"
    "?var-r8rg67rn=21d4zvp1"
    "&var-wl33kewl=4qye4731"
    "&top=10"
)

response = requests.get(url)
response.raise_for_status()

data = response.json()

runs = data["data"]["runs"]

results = []

for item in runs:
    run = item["run"]

    player = run["players"][0]

    if player["rel"] == "user":
        player_response = requests.get(player["uri"])
        player_data = player_response.json()
        runner_name = player_data["data"]["names"]["international"]
    else:
        runner_name = player["name"]

    total_seconds = run["times"]["primary_t"]

    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    formatted_time = f"{minutes}:{seconds:06.3f}"

    results.append({
        "Rank": item["place"],
        "Speedrunner": runner_name,
        "Time": formatted_time,
        "Version": "1.16-1.19",
        "Date": run["date"]
    })

df = pd.DataFrame(results)

print(df)