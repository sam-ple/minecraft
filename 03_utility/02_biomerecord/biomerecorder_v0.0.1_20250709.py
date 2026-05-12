import minescript as m
import time

m.execute("/locate biome plains")
m.execute("/locate biome desert")
m.execute("/locate biome forest")
m.execute("/locate biome savanna")
m.execute("/locate biome taiga")

# チェック対象のバイオーム一覧
BIOMES_TO_CHECK = [
    "minecraft:plains",
    "minecraft:desert",
    "minecraft:forest",
    "minecraft:savanna",
    "minecraft:taiga",
]

def check_biomes(biome_list):
    x, y, z = map(int, m.player_position())
    for biome_id in biome_list:
        # 条件にマッチしたらチャットに出力
        m.execute(f"/execute if biome {x} {y} {z} {biome_id} run say You are in {biome_id}")

# メインループ：2秒おきにチェック
while True:
    check_biomes(BIOMES_TO_CHECK)
    time.sleep(2)
