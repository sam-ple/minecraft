import minescript as m
import random
import time

# 変換候補リスト
random_items = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
    "minecraft:carrot",
    "minecraft:bread"
]

m.echo("Quartz Block Randomizer is running!")

while True:
    # インベントリ取得
    for item in m.player_inventory():
        if item.item == "minecraft:quartz_block":
            # ランダムアイテムに変換
            new_item = random.choice(random_items)
            target_slot = item.slot - 9  # ホットバー分ずらす
            m.execute(f"/item replace entity @p inventory.{target_slot} with {new_item} {item.count}")
            m.echo(f"Quartz block in slot {item.slot} → {new_item}!")

    time.sleep(0.5)  # 適度に待つ
