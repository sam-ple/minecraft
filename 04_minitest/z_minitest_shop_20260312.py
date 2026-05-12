import minescript as m

# ==================================================
# TEST NPC　テスト用村人ショップ
# ==================================================

# 村人
# スノーボール販売
# 1エメラルド → 1スノーボール
#
# Silent → 声なし
# Invulnerable → 無敵
# NoAI → 動かない

# m.execute('/summon villager ~-1 ~ ~-5 {"VillagerData":{"level":5,"profession":"farmer","type":"plains"},"Silent":true,"Invulnerable":true,"NoAI":true,"Offers":{"Recipes":[{"buy":{"id":"emerald","count":1},"sell":{"id":"snowball","count":1},"maxUses":9999}]}}')

# X, Y, Z = "~", "~", "~-5"  # 村人の出現座標（例）
# m.execute(f'''
#     summon villager {X} {Y} {Z} {{
#     VillagerData:{{level:5,profession:"farmer",type:"plains"}},
#     Silent:1b,
#     Invulnerable:1b,
#     NoAI:1b,
#     Offers:{{Recipes:[{{buy:{{id:"minecraft:emerald",Count:1b}},sell:{{id:"minecraft:snowball",Count:1b}},maxUses:9999}}]}}
# }}
# '''.replace("\n",""))

# 座標
X, Y, Z = "~", "~", "~-5"

# 取引内容
buy_item = "emerald"
buy_count = 1

sell_item = "snowball"
sell_count = 1

m.execute(
    f'/summon villager {X} {Y} {Z} '
    '{'
    'VillagerData:{level:5,profession:"farmer",type:"plains"},'
    'Silent:1b,'
    'Invulnerable:1b,'
    'NoAI:1b,'
    'Offers:{Recipes:['
        '{'
        f'buy:{{id:"minecraft:{buy_item}",Count:{buy_count}b}},'
        f'sell:{{id:"minecraft:{sell_item}",Count:{sell_count}b}},'
        'maxUses:9999'
        '}'
    ']}'
    '}'
)

def summon_shop(x, y, z, buy_item, buy_count, sell_item, sell_count):

    m.execute(
        f'/summon villager {x} {y} {z} '
        '{'
        'VillagerData:{level:5,profession:"farmer",type:"plains"},'
        'Silent:1b,Invulnerable:1b,NoAI:1b,'
        'Offers:{Recipes:['
        '{'
        f'buy:{{id:"minecraft:{buy_item}",Count:{buy_count}b}},'
        f'sell:{{id:"minecraft:{sell_item}",Count:{sell_count}b}},'
        'maxUses:9999'
        '}'
        ']}'
        '}'
    )

summon_shop("~","~","~-5","emerald",1,"snowball",1)
