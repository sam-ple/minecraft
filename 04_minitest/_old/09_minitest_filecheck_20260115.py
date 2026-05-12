import os
import json

DIR = "minescript/data"

if os.path.isfile(f"{DIR}/biome.json"):
    with open(f"{DIR}/biome.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Load successful")
else:
    print("biome.json not found")
