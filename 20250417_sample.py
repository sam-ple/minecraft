import minescript
import sys
import time

if len(sys.argv) < 2:
    minescript.echo("コマンドを指定してください。")
    sys.exit(1)

user_input = sys.argv[1]

# ------------------------------------------------------------
# 設定
# ------------------------------------------------------------
map_time = {
    "hinode": "sunrise",
    "hiru": "day",
    "shogo": "noon",
    "yuugure": "sunset",
    "yoru": "night",
    "shinya": "midnight",
}

map_weather = {
    "hare": "clear",
    "ame": "rain",
    "raiu": "thunder",
}

map_gamemode = {
    "sumode": "survival",
    "crmode": "creative",
    "spmode": "spectator",
    "admode": "adventure",
}

# 方角マッピング（東西南北のY軸回転値）
map_direction = {
    "north": 180,
    "south": 0,
    "east": -90,
    "west": 90
}

# ============================================================
# 関数：配信用設定
# ============================================================
def mode():
#    minescript.execute('/title @a title {"text":"配信用設定","color":"yellow","bold":true}')
    map_settings = {
        "keepInventory": "true",
        "doDaylightCycle": "false",
        "doMobSpawning": "false",
    }
    for rule, value in map_settings.items():
        minescript.execute(f"/gamerule {rule} {value}")
    minescript.execute("/time set day")      # 時間を昼に
    minescript.execute("/weather clear")     # 天気を晴れに
    minescript.echo("「配信用設定」を適用しました！（キープインベントリ＋常に昼＋モブ湧きオフ）")

# ============================================================
# 関数：複数モブ召喚
# ============================================================
def mobs():
#    minescript.execute('/title @a title {"text":"友好MOB召喚！","color":"light_purple","bold":true}')
    
    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()

    # 各Mobとオフセットのリスト（Mob名, Xオフセット, Zオフセット, NBT）
    mob_list = [
        ("sheep", 1, 1, "{Color:6}"),  # ピンクの羊（Color:6）
        ("allay", 2, 2, "{}"),        # アレイ
        ("cow", 3, 3, "{}"),
        ("chicken", 4, 4, "{}"),
        ("bee", 5, 5, "{}"),
        ("parrot", -1, -1, "{Variant:0}"),
        ("parrot", -2, -2, "{Variant:1}"),
        ("parrot", -3, -3, "{Variant:2}"),
        ("parrot", -4, -4, "{Variant:3}"),
        ("parrot", -5, -5, "{Variant:4}"),
        ("fox", -6, -6, "{Type:\"red\"}"),  # 赤キツネ
        ("rabbit", -7, -7, "{}")
    ]

    # 各Mobをスポーン
    for mob, dx, dz, nbt in mob_list:
        sx = x + dx
        sz = z + dz
        minescript.execute(f'/summon minecraft:{mob} {sx} {y} {sz} {nbt}')

    minescript.echo("Mobを召喚しました！")

# ============================================================
# 関数：花火
# ============================================================
def fireworks():
#    minescript.execute('/title @a title {"text":"花火を打ち上げる","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y + 2), int(z)  # プレイヤーの少し上

    minescript.execute(f"summon firework_rocket {x} {y+2} {z} {{LifeTime:20}}")
    minescript.execute(f"summon firework_rocket {x+1} {y+2} {z} {{LifeTime:20}}")
    minescript.execute(f"summon firework_rocket {x-1} {y+2} {z} {{LifeTime:20}}")
    minescript.echo("花火を打ち上げたよ！")


# ============================================================
# 関数：チートパック
# ============================================================
def cheatpack():
#    minescript.execute('/title @a title {"text":"チート装備一式を渡す","color":"yellow","bold":true}')
    # ダイヤ装備をそれぞれの装備スロットにセット
    minescript.execute('/item replace entity @p weapon.mainhand with minecraft:diamond_sword')
    minescript.execute('/item replace entity @p armor.head with minecraft:diamond_helmet')
    minescript.execute('/item replace entity @p armor.chest with minecraft:diamond_chestplate')
    minescript.execute('/item replace entity @p armor.legs with minecraft:diamond_leggings')
    minescript.execute('/item replace entity @p armor.feet with minecraft:diamond_boots')
    
    # ツール類（ピッケル・斧・シャベル）はホットバーに配布
    map_tools = [
        'minecraft:diamond_pickaxe',
        'minecraft:diamond_axe',
        'minecraft:diamond_shovel'
    ]
    for tool in map_tools:
        minescript.execute(f'/give @p {tool} 1')

    # 食べ物（各64個）を配布
    map_foods = [
        'minecraft:golden_apple',
        'minecraft:enchanted_golden_apple',
        'minecraft:cooked_beef'
    ]
    for food in map_foods:
        minescript.execute(f'/give @p {food} 64')

    # ブロック類（各64個）を配布
    map_blocks = [
        'minecraft:torch',
        'minecraft:oak_planks',
        'minecraft:cobblestone',
    ]
    for block in map_blocks:
        minescript.execute(f'/give @p {block} 64')

    minescript.echo("チート装備を配布しました。")

# ============================================================
# 関数：ネザーゲート
# ============================================================
def nethergate():
#    minescript.execute('/title @a title {"text":"ネザーゲートを設置","color":"red","bold":true}')
    
    x, y, z = minescript.player_position()
    minescript.execute(f"/tp @p {x} {y} {z} 0 0")  # 南向きに
    x, y, z = int(x - 7), int(y), int(z + 3)  # プレイヤーの前方に設置

    # ネザーゲートのフレーム（高さ5 × 幅4）
    for dy in range(5):
        for dx in range(4):
            bx = x + dx
            by = y + dy
            bz = z
            # 黒曜石を枠にだけ設置、それ以外は空洞
            if dx == 0 or dx == 3 or dy == 0 or dy == 4:
                minescript.execute(f"/setblock {bx} {by} {bz} minecraft:obsidian")
            else:
                minescript.execute(f"/setblock {bx} {by} {bz} minecraft:air")

    # 下から2段目の内側に火をつけてポータルを起動
    minescript.execute(f"/setblock {x + 1} {y + 1} {z} minecraft:fire")

    minescript.echo("ネザーゲートを作成・起動したよ！")

# ============================================================
# 関数：スタート
# ============================================================
def start():
    # カウントダウン
    for count, color in [("3", "red"), ("2", "gold"), ("1", "yellow")]:
        minescript.execute(f'/title @a title {{"text":"{count}","color":"{color}","bold":true}}')
        time.sleep(1)

    # スタート！
    minescript.execute('/title @a title {"text":"スタート！","color":"green","bold":true}')

    minescript.echo("スタートしました！")


# ============================================================
# 関数：整地
# ============================================================
def flatten():
#    minescript.execute('/title @a title {"text":"整地","color":"red","bold":true}')
    x, y, z = map(int, minescript.player_position())

    width = 20
    height = 20

    for dx in range(-(width//2), width//2):
        for dy in range(-1, height + 1): 
            for dz in range(-(width//2), width//2):
                bx, by, bz = x + dx, y + dy, z + dz

                # 地面（足元）をブロックにする
                if dy == -1:
                    minescript.execute(f"setblock {bx} {by} {bz-1} stripped_pale_oak_wood")
                else:
                    minescript.execute(f"setblock {bx} {by} {bz} air")

    minescript.echo("整地しました。")

# ============================================================
# 関数：ベースキット
# ============================================================
def base_kit():
#    minescript.execute('/title @a title {"text":"ベースキットを設置","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    minescript.execute(f"/tp @p {x} {y} {z} 0 0")  # 南向きに
    x, y, z = int(x), int(y), int(z + 3)

    # 並べて設置
    minescript.execute(f"setblock {x + 2} {y} {z} minecraft:crafting_table")
    minescript.execute(f"setblock {x + 3} {y} {z} minecraft:furnace")
    minescript.execute(f"setblock {x + 4} {y} {z} minecraft:chest")

    minescript.echo("作業キットを設置したよ！")

# ============================================================
# 関数：ドロッパー
# ============================================================
def dropper():
#    minescript.execute('/title @a title {"text":"ドロッパーを設置","color":"gold","bold":true}')
    
    x, y, z = map(int, minescript.player_position())
    minescript.execute(f"/tp @p {x} {y} {z} 0 0")  # 南向きに

    # プレイヤーの南側（前方）
    dx, dz = 0, 3
    dropper_x = x + dx
    dropper_y = y + 1
    dropper_z = z + dz

    # ① ドロッパーを設置（プレイヤーが南向き）
    minescript.execute(f"/setblock {dropper_x} {dropper_y} {dropper_z} minecraft:dropper[facing=north]")

    # ② ドロッパーの下に土台ブロックを設置
    minescript.execute(f"/setblock {dropper_x} {dropper_y - 1} {dropper_z} minecraft:polished_diorite")

    # ③ ドロッパーにボタンを設置
    minescript.execute(f"/setblock {dropper_x} {dropper_y - 1} {dropper_z - 1} minecraft:polished_blackstone_button[facing=north]")

    # ④ ドロッパーにアイテム追加
    items = [
        {"id": "yellow_concrete", "Count": 2},
        {"id": "light_blue_concrete", "Count": 2},
        {"id": "red_concrete", "Count": 2},
    ]
    nbt_items = ",".join([
        f'{{Slot:{i}b,id:"minecraft:{item["id"]}",Count:{item["Count"]}b}}'
        for i, item in enumerate(items)
    ])
    minescript.execute(f"/data merge block {dropper_x} {dropper_y} {dropper_z} {{Items:[{nbt_items}]}}")

    minescript.echo("ドロッパーを設置完了！")

# ============================================================
# 関数：テレポート
# ============================================================
def teleport():
    x, y, z = map(int, minescript.player_position())

    # プレイヤーを南向きに（基準を固定）
    minescript.execute(f"/tp @p {x} {y} {z} 0 0")

    # プレイヤーの南側（前方）
    dx, dz = -2, 3
    block_x = x + dx
    block_y = y + 1
    block_z = z + dz

    minescript.execute(f"/setblock {block_x} {block_y} {block_z} minecraft:pale_oak_wood")
    minescript.execute(f"/setblock {block_x} {block_y - 1} {block_z} minecraft:pale_oak_wood")
    minescript.execute(f"/setblock {block_x} {block_y - 1} {block_z - 1} minecraft:pale_oak_button[facing=north]")
    minescript.execute(f"/setblock {block_x} {block_y} {block_z - 1} minecraft:pale_oak_wall_sign[facing=north]{{Text1:'{{\"text\":\"テレポート\"}}'}}")
    # コマンドブロックを設置（地下）
    minescript.execute(f"/setblock {block_x} {block_y - 2} {block_z} minecraft:command_block")
    # 中身のコマンドを設定（テレポート）
    minescript.execute(f"/data merge block {block_x} {block_y - 2} {block_z} {{Command:'/tp @p 1079 119 1102'}}")
    minescript.echo("テレポート台を設置しました！")

# ============================================================
# 関数：現在地
# ============================================================
def where():
#    minescript.execute('/title @a title {"text":"プレイヤーの現在位置","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    minescript.echo(f"現在位置: X={int(x)}, Y={int(y)}, Z={int(z)}")

# ============================================================
# 関数：バイオーム座標
# ============================================================
def biome():
#    minescript.execute('/title @a title {"text":"バイオーム座標を取得","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z)

    map_biomes = ["minecraft:desert", "minecraft:forest", "minecraft:taiga", "minecraft:swamp", "minecraft:plains", "minecraft:pale_garden"]
    
    for biome in map_biomes:
        minescript.execute(f'/locate biome {biome}')

# ------------------------------------------------------------
# ヘルプ
# ------------------------------------------------------------
if user_input == "help":
    text_help = """
    ヘルプ表示
    """
    minescript.echo(text_help)

# ------------------------------------------------------------
# 時間
# ------------------------------------------------------------
elif user_input in map_time:
    minescript.execute(f"/time set {map_time[user_input]}")
    minescript.echo(f"時間を「{user_input}」に設定しました。")

# ------------------------------------------------------------
# 天気
# ------------------------------------------------------------
elif user_input in map_weather:
    minescript.execute(f"/weather {map_weather[user_input]}")
    minescript.echo(f"天気を「{user_input}」に設定しました。")

# ------------------------------------------------------------
# ゲームモード
# ------------------------------------------------------------
elif user_input in map_gamemode:
    minescript.execute(f"/gamemode {map_gamemode[user_input]}")
    minescript.echo(f"ゲームモードを「{user_input}」に変更しました。")

# ------------------------------------------------------------
# 準備
# ------------------------------------------------------------
elif user_input == "prepare":
    x, y, z = map(int, minescript.player_position())
    minescript.execute(f"/tp @p {x} {y} {z} 0 0")  # 南向きに
    flatten()
    base_kit()
    nethergate()
    dropper()
    teleport()

# ------------------------------------------------------------
# スタートパック
# ------------------------------------------------------------
elif user_input == "startpack":
    mode()
    cheatpack()
    mobs()
    fireworks()
    start()

# ------------------------------------------------------------
# スタート
# ------------------------------------------------------------
elif user_input == "start":
    start()

# ------------------------------------------------------------ 
# 画面を真っ暗にするエンド効果
# ------------------------------------------------------------
elif user_input == "end":
    minescript.execute('/title @a title {"text":"終了","color":"dark_red","bold":true}')
    minescript.execute('/effect give @a minecraft:blindness 10 1 true')
    minescript.echo("終了...")

# ------------------------------------------------------------
# 配信用設定
# ------------------------------------------------------------
elif user_input == "mode":
    mode()

# ------------------------------------------------------------
# 帰還
# ------------------------------------------------------------
elif user_input == "return":
    minescript.execute(f"/tp @p -27 64 5")

# ------------------------------------------------------------
# インベントリ全削除
# ------------------------------------------------------------
elif user_input == "clearitem":
    minescript.execute('/title @a title {"text":"インベントリ全削除","color":"yellow","bold":true}')
    minescript.execute('/clear @p')
    minescript.echo("インベントリをすべて削除しました。")

# ------------------------------------------------------------
# 整地
# ------------------------------------------------------------
elif user_input == "flatten":
    flatten()

# ------------------------------------------------------------
# 最強の釣り竿
# ------------------------------------------------------------
elif user_input == "fishrod":
    minescript.execute('/title @a title {"text":"最強の釣り竿を渡す","color":"yellow","bold":true}')
    # メインハンド（ホットバーのスロット0）に直接渡す
    minescript.execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')
    
    # 釣り竿にエンチャントを追加
    map_enchants = [
        "minecraft:luck_of_the_sea 3",
        "minecraft:lure 3",
        "minecraft:unbreaking 3",
        "minecraft:mending 1"
    ]
    for ench in map_enchants:
        minescript.execute(f"/enchant @p {ench}")
    
    minescript.echo("最強の釣り竿を渡しました。")

# ------------------------------------------------------------
# チート装備一式（ダイヤ装備＆自動装備＆食べ物64個）
# ------------------------------------------------------------
elif user_input == "cheatpack":
    cheatpack()

# ------------------------------------------------------------ 
# 周囲にフレンドリーな動物を召喚
# ------------------------------------------------------------ 
elif user_input == "animals":
    animals()

# ------------------------------------------------------------ 
# プレイヤーがジャンプした回数をカウント 
# ------------------------------------------------------------ 
elif user_input == "count":
    minescript.execute('/title @a title {"text":"カウント開始","color":"yellow","bold":true}')
    minescript.execute('/scoreboard objectives add Jump minecraft.custom:minecraft.jump "ジャンプした回数"')
    # ★スコアボードを表示
    minescript.execute('/scoreboard objectives setdisplay sidebar Jump')
    minescript.echo("ジャンプをカウントします。")

# ------------------------------------------------------------ 
# ジャンプした回数のカウントをリセット
# ------------------------------------------------------------ 
elif user_input == "resetcount":
    minescript.execute('/title @a title {"text":"カウントリセット","color":"yellow","bold":true}')
    minescript.execute('/scoreboard players set @a Jump 0')
    minescript.echo("ジャンプのカウントをリセットしました。")

# ------------------------------------------------------------ 
# ジャンプした回数のカウントを解除
# ------------------------------------------------------------ 
elif user_input == "nocount":
    minescript.execute('/title @a title {"text":"カウント解除","color":"yellow","bold":true}')
    minescript.execute('/scoreboard objectives remove Jump')
    minescript.echo("ジャンプのカウントを解除しました。")

# ------------------------------------------------------------
# タワー
# ------------------------------------------------------------
elif user_input == "tower":
    x, y, z = map(int, minescript.player_position())

    # 5つのペールオークを積み上げる
    for i in range(10):
        minescript.execute(f"/setblock {x} {y + i} {z} minecraft:stripped_oak_log")

    # プレイヤーを一番上の上にテレポート（5段上）
    minescript.execute(f"/tp @p {x + 0.5} {y + 10} {z + 0.5}")

    minescript.echo("塔を建てて、上に移動しました！")

# ------------------------------------------------------------
# ドット絵
# ------------------------------------------------------------
elif user_input == "dot":
    minescript.execute('/title @a title {"text":"ニワトリのドット絵を作成","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
#    yaw = minescript.player_rotation()
    x, y, z = int(x), int(y), int(z + 5)  # プレイヤーの前方空中に描画

    map_dot = [
        "GGGWWWWGGG",
        "GGGBWWBGGG",
        "GGWYYYYWGG",
        "GWWYYYYWWG",
        "GWWWRRWWWG",
        "GWWWRRWWWG",
        "GGWWWWWWGG",
        "GGWWWWWWGG",
        "GGGYGGYGGG",
        "GGGYGGYGGG",
    ]

    map_color = {
        "W": "white_wool",
        "B": "black_wool",
        "Y": "yellow_wool",
        "R": "red_wool",
        "G": "light_gray_wool",
    }

    for dy, row in enumerate(map_dot):
        for dx, char in enumerate(row):
            block = map_color.get(char)
            if block:
                bx = x + dx - 5  # 中央に寄せる（10文字→-5）
                by = y + 9 - dy  # 上から下に描画（10段）
                minescript.execute(f"/setblock {bx} {by} {z} minecraft:{block}")

    minescript.echo("ニワトリを空に描いたよ！🐔")

# ------------------------------------------------------------ 
# ドット絵を削除 
# ------------------------------------------------------------ 
elif user_input == "cleardot":
    minescript.execute('/title @a title {"text":"ドット絵を削除","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z + 5)  # プレイヤーの前の空中

    # ドット絵の範囲に合わせて削除
    map_dot_width = 10  # 横の長さ（"GGGWWWWGGG" なので10）
    map_dot_height = 10  # 縦の長さ（10行）

    for dy in range(map_dot_height):
        for dx in range(map_dot_width):
            bx = x + dx - 5  # -5 で中央寄せ
            by = y + 9 - dy  # 上から下へ
            minescript.execute(f"/setblock {bx} {by} {z} minecraft:air")

    minescript.echo("ドット絵を消去したよ🧹")

# ------------------------------------------------------------
# ドロッパー
# ------------------------------------------------------------
elif user_input == "dropper":
    dropper()

# ------------------------------------------------------------
# テレポート
# ------------------------------------------------------------
elif user_input == "teleport":
    teleport()

# ------------------------------------------------------------
# 花火を打ち上げる
# ------------------------------------------------------------
elif user_input == "fireworks":
    fireworks()

# ------------------------------------------------------------
# 作業台・かまど・チェストセットを配置
# ------------------------------------------------------------
elif user_input == "base_kit":
    base_kit()

# ------------------------------------------------------------
# プレイヤーの現在位置を表示
# ------------------------------------------------------------
elif user_input == "where":
    where()

# ------------------------------------------------------------
# 方角を変える
# ------------------------------------------------------------
elif user_input in map_direction:
    angle = map_direction[user_input]
    minescript.execute('/title @a title {"text":"方角を変える","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    minescript.execute(f"/tp @p {x} {y} {z} {angle} 0")
    minescript.echo(f"方角を {user_input} に変更しました（Yaw: {angle}）")

# ------------------------------------------------------------
# プレイヤーの位置から最寄りのバイオーム座標をまとめて表示
# ------------------------------------------------------------
elif user_input == "biome":
    biome()

# ------------------------------------------------------------ 
# ネザーゲートを生成＆着火
# ------------------------------------------------------------ 
elif user_input == "nethergate":
    nethergate()

# ------------------------------------------------------------
# 装備
# ------------------------------------------------------------
elif user_input == "armor":
    minescript.execute('/item replace entity @p weapon.mainhand with minecraft:diamond_sword')
    minescript.execute('/item replace entity @p armor.head with minecraft:diamond_helmet')
    minescript.execute('/item replace entity @p armor.chest with minecraft:diamond_chestplate')
    minescript.execute('/item replace entity @p armor.legs with minecraft:diamond_leggings')
    minescript.execute('/item replace entity @p armor.feet with minecraft:diamond_boots')
    minescript.execute('/item replace entity @p weapon.offhand with minecraft:shield') 

# ------------------------------------------------------------
# アーマースタンド
# ------------------------------------------------------------
elif user_input == "armorstand":
    x, y, z = map(int, minescript.player_position())
    minescript.execute(f"/tp @p {x} {y} {z} 0 0")  # 南向きに

    # 左（東） - ネザライト装備 + トライデント
    left_nbt = (
        '{Invisible:0b,ShowArms:1b,ArmorItems:['
        '  {id:"minecraft:netherite_boots",Count:1b},'
        '  {id:"minecraft:netherite_leggings",Count:1b},'
        '  {id:"minecraft:netherite_chestplate",Count:1b},'
        '  {id:"minecraft:netherite_helmet",Count:1b}'
        '],HandItems:['
        '  {id:"minecraft:trident",Count:1b},{}]}'
    )
    minescript.execute(f'/summon armor_stand {x+1} {y} {z} {left_nbt}')

    # 右（西） - 金装備 + クロスボウ
    right_nbt = (
        '{Invisible:0b,ShowArms:1b,ArmorItems:['
        '  {id:"minecraft:golden_boots",Count:1b},'
        '  {id:"minecraft:golden_leggings",Count:1b},'
        '  {id:"minecraft:golden_chestplate",Count:1b},'
        '  {id:"minecraft:golden_helmet",Count:1b}'
        '],HandItems:['
        '  {id:"minecraft:crossbow",Count:1b},{}]}'
    )
    minescript.execute(f'/summon armor_stand {x-1} {y} {z} {right_nbt}')

# ------------------------------------------------------------
# アーマースタンドを削除
# ------------------------------------------------------------
elif user_input == "reset_armorstand":
    minescript.execute('kill @e[type=minecraft:armor_stand]')
#    minescript.execute('kill @e[type=minecraft:armor_stand,limit=1,sort=nearest]')

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    minescript.echo(f"未対応のコマンドです: {user_input}")
