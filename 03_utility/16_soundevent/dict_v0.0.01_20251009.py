from bs4 import BeautifulSoup
import requests
import json

url = "https://mappings.dev/1.21.9/net/minecraft/sounds/SoundEvents.html"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

records = []

# 各 SoundEvent 定義を抽出
for tr in soup.select("table.N.O tbody tr"):
    inner = tr.select("table tbody tr")
    if len(inner) < 5:
        continue

    entry = {
        "obfuscated": inner[0].select_one(".G").text.strip(),
        "mojang": inner[1].select_one(".G").text.strip(),
        "intermediary": inner[2].select_one(".G").text.strip(),
        "yarn": inner[3].select_one(".G").text.strip(),
        "searge": inner[4].select_one(".G").text.strip(),
    }

    records.append(entry)

# 保存
with open("soundevents_mapping.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

# テスト出力
print(records[:3])  # 最初の3件だけ確認
