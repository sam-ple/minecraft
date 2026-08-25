import minescript as m

m.execute("give @a minecraft:carrot_on_a_stick")
m.execute("give @a minecraft:clock")

# ==============================
# 基本設定（キープインベントリ）
# ==============================
m.execute("gamerule keepInventory true")

# ==============================
# ハート2倍（最大体力変更）
# 20 = 通常（ハート10個）
# 40 = ハート20個
# ==============================
m.execute("attribute @a minecraft:max_health base set 40")

# ==============================
# ネザライト装備一式
# ==============================
m.execute("give @a netherite_sword")

# 自動装備（装備スロットに直接入れる）
m.execute("item replace entity @a armor.head with minecraft:netherite_helmet")
m.execute("item replace entity @a armor.chest with minecraft:netherite_chestplate")
m.execute("item replace entity @a armor.legs with minecraft:netherite_leggings")
m.execute("item replace entity @a armor.feet with minecraft:netherite_boots")

# ==============================
# 永続暗視
# ==============================
m.execute("effect give @a minecraft:night_vision infinite 0 true")
