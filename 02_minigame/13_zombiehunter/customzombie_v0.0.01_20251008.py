import minescript as m

# ==============================
# ゾンビ定義リスト
# ==============================
zombies = [
    {
        "name": "展示用ゾンビ",
        "y_offset": 1,
        "NoAI": True,
        "mainhand": None,
        "armor": [
            {"slot": "head", "id": "minecraft:diamond_helmet", "count": 1},
            None, None, None
        ]
    },
    {
        "name": "装備フルゾンビ",
        "y_offset": 1,
        "NoAI": False,
        "mainhand": {"id": "minecraft:diamond_sword", "count": 1, "enchantments":{"sharpness":5}},
        "armor": [
            {"slot": "boots", "id": "minecraft:diamond_boots", "count":1},
            {"slot": "leggings", "id": "minecraft:diamond_leggings", "count":1},
            {"slot": "chestplate", "id": "minecraft:diamond_chestplate", "count":1},
            {"slot": "head", "id": "minecraft:diamond_helmet", "count":1}
        ]
    },
    {
        "name": "火属性ゾンビ",
        "y_offset": 1,
        "NoAI": False,
        "mainhand": {"id": "minecraft:blaze_rod", "count": 1, "enchantments": {"fire_aspect":2}},
        "armor": [None,None,None,None]
    }
]

# ==============================
# ゾンビ生成ループ
# ==============================
for z in zombies:
    cmd = '/summon zombie ~ ~{} ~ {{PersistenceRequired:1'.format(z["y_offset"])
    
    # AI 無効
    if z["NoAI"]:
        cmd += ',NoAI:1b'
    
    # メインハンド装備
    if z["mainhand"]:
        main = z["mainhand"]
        enchants = ""
        if "enchantments" in main:
            enchants = ",".join(f'{k}:{v}' for k,v in main["enchantments"].items())
            enchants = f'{{enchantments:{{{enchants}}}}}'
        cmd += f',equipment:{{mainhand:{{id:"{main["id"]}",count:{main["count"]}b,components:{enchants}}}}}'
    
    # アーマー装備
    if "armor" in z:
        armor_list = []
        for slot in z["armor"]:
            if slot:
                armor_list.append(f'{{id:"{slot["id"]}",Count:{slot["count"]}b}}')
            else:
                armor_list.append('{}')
        # Minecraft 1.21系なら ArmorItems に直接入れる
        cmd += f',ArmorItems:[{",".join(armor_list)}]'
    
    cmd += '}'
    
    m.execute(cmd)
    m.echo(f'{z["name"]} を召喚しました')
