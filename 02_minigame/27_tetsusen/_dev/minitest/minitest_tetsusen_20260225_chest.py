# Face SOUTH (+Z direction) before running this script
# /give @p diamond_pickaxe 1
# /enchant @p efficiency 5
# /enchant @p fortune 3
# /data get entity @p SelectedItem
# /give @p diamond_pickaxe[enchantments={"minecraft:efficiency":5,"minecraft:fortune":3}] 1

import minescript as m
import math

px, py, pz = m.player().position
x, y, z = math.floor(px), math.floor(py), math.floor(pz)
cx, cy, cz = x, y, z-2

# -------------------------
# ダブルチェスト設置
# -------------------------

m.execute(f"setblock {cx-2} {cy} {cz} minecraft:chest[facing=south,type=right]")
m.execute(f"setblock {cx-1} {cy} {cz} minecraft:chest[facing=south,type=left]")


# m.execute(f"data remove block {cx-1} {cy} {cz} Items")
# m.execute(f"data remove block {cx} {cy} {cz} Items")

# -------------------------
# 1.21 components形式
# -------------------------

# pickaxe_item = (
#     '{id:"minecraft:diamond_pickaxe",count:1,components:{'
#     '"minecraft:enchantments":{levels:{'
#     '"minecraft:efficiency":5,'
#     '"minecraft:fortune":3'
#     '}}}}'
# )

# # -------------------------
# # 右チェスト（cx-1）
# # -------------------------

# for slot in range(27):
#     m.execute(
#         f'data modify block {cx-1} {cy} {cz} Items append value '
#         f'{{Slot:{slot}b,{pickaxe_item}}}'
#     )

# # -------------------------
# # 左チェスト（cx）
# # -------------------------

# for slot in range(27):
#     m.execute(
#         f'data modify block {cx} {cy} {cz} Items append value '
#         f'{{Slot:{slot}b,{pickaxe_item}}}'
#     )

for slot in range(27):
    m.execute(
        f'item replace block {cx-2} {cy} {cz} container.{slot} '
        f'with minecraft:diamond_pickaxe'
        f'[enchantments={{"minecraft:efficiency":5,"minecraft:fortune":3}}] 1'
    )

for slot in range(27):
    m.execute(
        f'item replace block {cx-1} {cy} {cz} container.{slot} '
        f'with minecraft:diamond_pickaxe'
        f'[enchantments={{"minecraft:efficiency":5,"minecraft:fortune":3}}] 1'
    )

m.echo("Double chest filled correctly (1.21 format)!")
