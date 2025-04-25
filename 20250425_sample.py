# -------------------------
# 標準ライブラリ
# -------------------------
from sys import (argv, exit)
from time import sleep
import random
import math
from datetime import datetime

# -------------------------
# 外部ライブラリ
# -------------------------
import minescript
from minescript import (execute, echo)


arg1 = argv[1] if len(argv) > 1 else (echo("コマンドを指定してください。") or exit(1))
arg2 = argv[2] if len(argv) > 2 else None  # 指定がなければ None

# ------------------------------------------------------------
# 帰還
# ------------------------------------------------------------
if arg1 == "return":
    execute(f"/tp @p -12 64 -136")

# ------------------------------------------------------------
# 1.21.5(minescriptが20250422に1.21.5に対応)
# ------------------------------------------------------------
elif arg1 == "1.21.5":
    if arg2 == "mobs":
        x, y, z = minescript.player_position()
        execute(f"/tp @p {x} {y} {z} -180 45")  # 南向きに向ける
        z = z-3

        # タイトル表示
        execute('title @a title {"text":"1.21.5","color":"gold","bold":true}')
        execute('title @a subtitle {"text":"色違いのモブ","color":"aqua"}')
        
        # 色違いの牛
        execute(f'/summon minecraft:cow {x-3} {y} {z} {{variant:"warm"}}')
        execute(f'/summon minecraft:cow {x-2} {y} {z} {{variant:"cold"}}')

        # 色違いの豚
        execute(f'/summon minecraft:pig {x-1} {y} {z} {{variant:"warm"}}')
        execute(f'/summon minecraft:pig {x+1} {y} {z} {{variant:"cold"}}')

        # 色違いのニワトリ
        execute(f'/summon minecraft:chicken {x+2} {y} {z} {{variant:"warm"}}')
        execute(f'/summon minecraft:chicken {x+3} {y} {z} {{variant:"cold"}}')

        echo("🐖 1.21.5でアップデートされた色違いのモブたちを召喚しました！")

    elif arg2 == "spawnegg":
        # タイトル表示
        execute('title @a title {"text":"1.21.5","color":"gold","bold":true}')
        execute('title @a subtitle {"text":"スポーンエッグ","color":"light_purple"}')
        
        spawn_eggs = [
            "allay", "sniffer", "glow_squid", "tadpole", "axolotl", "strider",
            "camel", "frog", "vex", "phantom", "creeper", "warden", "blaze",
            "chicken", "panda"
        ]
        for mob in spawn_eggs:
            execute(f'/give @p minecraft:{mob}_spawn_egg 1')

        echo("🥚 1.21.5でアップデートされたスポーンエッグの一部を付与しました！")

# ------------------------------------------------------------
# スタート
# ------------------------------------------------------------
elif arg1 == "start":
    # Ready...
    execute('/title @a title {"text":"Ready...","color":"aqua","bold":true}')
    sleep(1)
    
    # 3, 2, 1 countdown with bell sound
    for count in ["3", "2", "1"]:
        execute(f'/title @a title {{"text":"{count}","color":"aqua","bold":true}}')
        execute('/playsound minecraft:block.bell.use master @a')
        sleep(1)
    
    # Go! with horn sound
    execute('/title @a title {"text":"Go!","color":"aqua","bold":true}')
    execute('/playsound minecraft:entity.pillager.celebrate master @a')
    sleep(0.5)
    
    echo("スタート！")

# ------------------------------------------------------------
# ミュージック
# ------------------------------------------------------------
elif arg1 == "music":
    # 癒し系BGM（静かな音楽）
    execute('/playsound minecraft:music.overworld.meadow music @p')
#    execute('/playsound minecraft:music.overworld.grove music @p')
#    execute('/playsound minecraft:music.overworld.forest music @p')
    echo("ミュージックスタート♬")

elif arg1 == "musicstop":
    execute('/stopsound @p music')
    echo("音楽を停止しました。")

# ------------------------------------------------------------
# エンド
# ------------------------------------------------------------
elif arg1 == "end":
    # 終了タイトル表示
    execute('/title @a title {"text":"終了！","color":"aqua","bold":true}')
    sleep(0.5)

    # 花火をプレイヤーの位置で打ち上げ（全員）
    execute('/execute as @a at @s run summon firework_rocket ~ ~1 ~ {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",Count:1,tag:{Fireworks:{Explosions:[{Type:1,Flicker:1,Colors:[11743532]}],Flight:1}}}}')

    # 花火音（補助）
    execute('/playsound minecraft:entity.firework_rocket.launch master @a')
    sleep(0.5)

    # プレイヤーをふわっと上昇（上方向にリフト）
    execute('/effect give @a minecraft:levitation 2 3 true')  # 2秒間、少し強めに

    # ゆっくり暗転（夜に）
    execute('/time set night')

    # エコーでメッセージ
    echo("終了！")

# ------------------------------------------------------------
# モブ召喚
# ------------------------------------------------------------
elif arg1 == "mobs":
    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()
    
    # アレイを出現させる数と半径
    num_allays = 24       # アレイの数（例：24体）
    radius = 5            # プレイヤーからの距離（円の半径）
    
    # 放射状にアレイを配置
    for i in range(num_allays):
        angle = 2 * math.pi * i / num_allays
        dx = round(math.cos(angle) * radius, 2)
        dz = round(math.sin(angle) * radius, 2)
        sx = x + dx
        sz = z + dz
        execute(f'/summon minecraft:allay {sx} {y} {sz} {{}}')
    
    # 視覚＆音の演出
    execute('/playsound minecraft:entity.allay.ambient_with_item master @a')
    
    echo("円形にアレイを召喚しました！")

# ------------------------------------------------------------
# 整地
# ------------------------------------------------------------
elif arg1 == "flatten":
    # ブロックの種類をarg2によって切り替え
    if arg2 == "1":
        block_type = "stripped_pale_oak_wood"
    elif arg2 == "2":
        block_type = "quartz_block"
    elif arg2 == "3":
        block_type = "gold_block"
    else:
        block_type = "grass_block"  # デフォルト fallback

    x, y, z = map(int, minescript.player_position())

    width = 20
    height = 20

    for dx in range(-(width // 2), width // 2):
        for dy in range(-1, height + 1):  # 足元の-1から整地
            for dz in range(-(width // 2), width // 2):
                bx, by, bz = x + dx, y + dy, z + dz

                if dy == -1:
                    execute(f"setblock {bx} {by} {bz} minecraft:{block_type}")
                else:
                    execute(f"setblock {bx} {by} {bz} minecraft:air")

    echo(f"{block_type} で整地しました。")
    execute('/tellraw @a {"text":"整地完了！","color":"aqua"}')

# ------------------------------------------------------------
# タワー
# ------------------------------------------------------------
elif arg1 == "tower":
    x, y, z = map(int, minescript.player_position())
    height = 10

    if arg2 == "1":
        block_type = "stripped_pale_oak_wood"
    elif arg2 == "2":
        block_type = "quartz_block"
    elif arg2 == "3":
        block_type = "grass_block"
    elif arg2 == "reset":
        block_type = None
    else:
        block_type = "stripped_pale_oak_wood"

    for i in range(height):
        if block_type:
            execute(f"/setblock {x} {y + i} {z} minecraft:{block_type}")
        else:
            # reset のとき、足元〜下に向かって壊す
            execute(f"/setblock {x} {y - i} {z} minecraft:air")

    if arg2 == "reset":
        # ゆっくり落下 + 落下ダメージ防止（5秒）
        execute("/effect give @p minecraft:slow_falling 5 0 true")
        # 耐性（軽減）
        # execute("/effect give @p minecraft:resistance 5 1 true")
        echo("🧹 タワーを破壊しました！ゆっくり落下中…")
    else:
        execute(f"/tp @p {x + 0.5} {y + height} {z + 0.5}")
        echo(f"🏗️ {block_type} のタワーを建てて上に移動しました！")

# ------------------------------------------------------------
# ドット絵
# ------------------------------------------------------------
elif arg1 == "dot":
    x, y, z = minescript.player_position()
    execute(f"/tp @p {x} {y} {z} 0 45")  # 南向きに向ける
    x, y, z = int(x), int(y), int(z + 5)

    # マップ定義（5層の3D）
    map_layers = [
        [  # 表面（0層目）
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
        ],
        [  # 表面（1層目）
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGYYYYGGG",
            "GGGYYYYGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
        ],
        [  # 中間（2層目）
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGYYYYGGG",
            "GGGYYYYGGG",
            "GGGGRRGGGG",
            "GGGGRRGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
        ],
        [  # 背面（3層目）
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
        ],
        [  # 背面（4層目）
            "GGGWWWWGGG",
            "GGGWWWWGGG",
            "GGWYYYYWGG",
            "GWWYYYYWWG",
            "GWWWRRWWWG",
            "GWWWRRWWWG",
            "GGWWWWWWGG",
            "GGWWWWWWGG",
            "GGGYGGYGGG",
            "GGGYGGYGGG",
        ],
    ]

    # 色のパターン定義（複数バージョン）
    color_patterns = [
        {
            "W": "white_wool", "B": "black_wool", "Y": "yellow_wool",
            "R": "red_wool", "G": "glass", "_": "air",
        },
        {
            "W": "white_wool", "B": "black_wool", "Y": "yellow_wool",
            "R": "red_wool", "G": "air", "_": "air",
        },
        {
            "W": "pink_wool", "B": "black_wool", "Y": "yellow_wool",
            "R": "red_wool", "G": "air", "_": "air",
        },
        {
            "W": "blue_wool", "B": "black_wool", "Y": "lime_wool",
            "R": "orange_wool", "G": "air", "_": "air",
        },
        {
            "W": "magenta_wool", "B": "gray_wool", "Y": "orange_wool",
            "R": "purple_wool", "G": "air", "_": "air",
        },
        {
            "W": "white_wool", "B": "black_wool", "Y": "yellow_wool",
            "R": "red_wool", "G": "air", "_": "air",
        },
    ]

    # 平面だけのレイヤー（中央の1層だけを使用）
    flat_layer = [map_layers[3]]  # 真ん中の層だけ

    if arg2 == "1":
        sleep(3)
        # 平面 × 1パターン
        map_color = color_patterns[0]
        for dz, layer in enumerate(flat_layer):  # dz = 0
            for dy, row in enumerate(layer):
                for dx, char in enumerate(row):
                    block = map_color.get(char)
                    if block:
                        bx = x + dx - 5
                        by = y + 9 - dy - 10
                        bz = z
                        execute(f"/setblock {bx} {by} {bz} minecraft:{block}")
        echo("平面ドットを表示したよ！🐥")

    elif arg2 == "2":
        sleep(3)
        # 3D × 1パターン
        map_color = color_patterns[0]
        for dz, layer in enumerate(map_layers):
            for dy, row in enumerate(layer):
                for dx, char in enumerate(row):
                    block = map_color.get(char)
                    if block:
                        bx = x + dx - 5
                        by = y + 9 - dy - 10
                        bz = z + dz
                        execute(f"/setblock {bx} {by} {bz} minecraft:{block}")
        echo("3Dニワトリ（1パターン）を表示！🐤")

    elif arg2 == "3":
        sleep(3)
        # 3D × 複数パターン（ループで順次変更）
        for i, map_color in enumerate(color_patterns):
            for dz, layer in enumerate(map_layers):
                for dy, row in enumerate(layer):
                    for dx, char in enumerate(row):
                        block = map_color.get(char)
                        if block:
                            bx = x + dx - 5
                            by = y + 9 - dy - 10
                            bz = z + dz
                            execute(f"/setblock {bx} {by} {bz} minecraft:{block}")
            echo(f"バージョン {i + 1} のニワトリ！🐔✨")
            sleep(2.5)

    else:
        echo("引数が正しくないよ！1～3 を指定してね。")

# ------------------------------------------------------------
# サイズ変更
# ------------------------------------------------------------
elif arg1 == "scale":
    scale_value = float(arg2) if arg2 else 1.0  # デフォルトで元のサイズに戻す
    execute(f"/attribute @s minecraft:scale base set {scale_value}")
    
    if scale_value == 1.0:
        echo("🔁 サイズを元に戻しました！")
    else:
        echo(f"📏 プレイヤーサイズを {scale_value} 倍に変更しました！")

# ------------------------------------------------------------
# 装備
# ------------------------------------------------------------
elif arg1 == "armor":
    execute('/item replace entity @p weapon.mainhand with minecraft:diamond_sword')
    execute('/item replace entity @p armor.head with minecraft:diamond_helmet')
    execute('/item replace entity @p armor.chest with minecraft:diamond_chestplate')
    execute('/item replace entity @p armor.legs with minecraft:diamond_leggings')
    execute('/item replace entity @p armor.feet with minecraft:diamond_boots')

    echo("ダイヤモンド装備を装着しました！")

# ------------------------------------------------------------
# ランダムな装備
# ------------------------------------------------------------
elif arg1 == "randomarmor":
    weapons = ["diamond_sword", "netherite_sword", "iron_axe", "bow", "crossbow"]
    helmets = ["diamond_helmet", "netherite_helmet", "iron_helmet", "golden_helmet", "leather_helmet"]
    chestplates = ["diamond_chestplate", "netherite_chestplate", "iron_chestplate", "golden_chestplate", "leather_chestplate"]
    leggings = ["diamond_leggings", "netherite_leggings", "iron_leggings", "golden_leggings", "leather_leggings"]
    boots = ["diamond_boots", "netherite_boots", "iron_boots", "golden_boots", "leather_boots"]
    shields = ["shield", "totem_of_undying", "bow", "torch", "ender_pearl"]

    execute(f'/item replace entity @p weapon.mainhand with minecraft:{random.choice(weapons)}')
    execute(f'/item replace entity @p armor.head with minecraft:{random.choice(helmets)}')
    execute(f'/item replace entity @p armor.chest with minecraft:{random.choice(chestplates)}')
    execute(f'/item replace entity @p armor.legs with minecraft:{random.choice(leggings)}')
    execute(f'/item replace entity @p armor.feet with minecraft:{random.choice(boots)}')
    execute(f'/item replace entity @p weapon.offhand with minecraft:{random.choice(shields)}')

    echo("ランダムな装備を装着しました！")

# ------------------------------------------------------------
# 馬
# ------------------------------------------------------------
# Tame:1b → 手懐け済み（これがないと乗れない）
# Saddled:1b → サドルが装備されてる状態
# NoAI:1b → 動かないように
# PersistenceRequired:1b → プレイヤーが離れても消えない
# - 普通の「馬（horse）」しか馬鎧は付けられない。
#   - スケルトンホース・ゾンビホースには馬鎧NG！
elif arg1 == "horse":
    x, y, z = map(int, minescript.player_position())

    # 通常の馬を召喚（手懐け済み＆サドル装備済み）
    horse_nbt = (
        '{Tame:1b, Saddled:1b}, '
        'PersistenceRequired:1b, NoAI:1b}'  
    )
    execute(f'/summon horse {x + 1} {y} {z} {horse_nbt}')
    echo("🐴 サドル付きで動かない馬を召喚！")

    # ダイヤモンドの馬鎧をプレイヤーに付与
    execute('/give @p minecraft:diamond_horse_armor')
    echo("💎 ダイヤの馬鎧をプレゼント！")

# elif arg1 == "aromorhorse":
#     x, y, z = map(int, minescript.player_position())

#     # サドル＋ダイヤ馬鎧＋手懐け済み＋動かない馬を召喚
#     horse_nbt = (
#         '{Tame:1b, Saddled:1b, '
#         'ArmorItems:[{Slot:2b,id:"minecraft:diamond_horse_armor",Count:1b}], '
#         'PersistenceRequired:1b, NoAI:1b}'
#     )
#     execute(f'/summon horse {x + 1} {y} {z} {horse_nbt}')
#     echo("🐎✨ ダイヤ馬鎧＆サドル付きの動かない馬を召喚！")

# ------------------------------------------------------------
# 鍛冶型装備
# ------------------------------------------------------------
elif arg1 == "smithkit":
    x, y, z = map(int, minescript.player_position())

    # 鍛冶台を足元のすぐ近くに出現
    execute(f'/setblock {x+1} {y} {z} minecraft:smithing_table')

    # 鍛冶型（Flow）x4（ヘルメット、チェスト、レギンス、ブーツ分）
    execute('/give @p minecraft:flow_armor_trim_smithing_template 4')

    # ネザライト防具一式
    armor_items = [
        "netherite_helmet",
        "netherite_chestplate",
        "netherite_leggings",
        "netherite_boots"
    ]
    for item in armor_items:
        execute(f'/give @p minecraft:{item}')

    # ダイヤモンド4個（装飾素材）
    execute('/give @p minecraft:diamond 4')

    # 説明
    echo("🛠 鍛冶台と装飾用アイテムをプレゼント！")

# 哨兵（Sentry）	minecraft:sentry
# 監視者（Watcher）	minecraft:watcher
# 荒れ地（Dune）	minecraft:dune
# 海辺（Coast）	minecraft:coast
# 丘陵（Tide）	minecraft:tide
# 大渓谷（Raiser）	minecraft:raiser
# 書庫（Wayfinder）	minecraft:wayfinder
# 野営地（Shaper）	minecraft:shaper
# 砦（Silence）	minecraft:silence
# 終焉（Spire）	minecraft:spire
# 裏地（Vex）	minecraft:vex
# フロー（Flow）	minecraft:flow
# elif arg1 == "smitharmor":
#     # 装飾付きネザライトヘルメット
#     nbt = '{Trim:{material:"minecraft:diamond",pattern:"minecraft:sentry"}}'
#     execute(f'/give @p minecraft:netherite_helmet{nbt} 1')
#     echo("✨装飾付きのネザライトヘルメットを付与！")

# ------------------------------------------------------------
# 最強の釣り竿
# ------------------------------------------------------------
elif arg1 == "fishrod":
    execute('/title @a title {"text":"最強の釣り竿を渡す","color":"yellow","bold":true}')
    # メインハンド（ホットバーのスロット0）に直接渡す
    execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')
    
    # 釣り竿にエンチャントを追加
    map_enchants = [
        "minecraft:luck_of_the_sea 3",
        "minecraft:lure 3",
        "minecraft:unbreaking 3",
        "minecraft:mending 1"
    ]
    for ench in map_enchants:
        execute(f"/enchant @p {ench}")
    
    echo("🎣 最強の釣り竿を渡しました！")

# elif arg1 == "fishrod":
#     # 最強の釣り竿を付与（宝釣りIII・入れ食いIII・耐久III・修繕I）
#     rod_command = (
#         '/give @p minecraft:fishing_rod{'
#         'Enchantments:['
#         '{"id":"minecraft:luck_of_the_sea","lvl":3},'
#         '{"id":"minecraft:lure","lvl":3},'
#         '{"id":"minecraft:unbreaking","lvl":3},'
#         '{"id":"minecraft:mending","lvl":1}'
#         ']} 1'
#     )
#     execute(rod_command)
#     echo("🎣 最強の釣り竿を手に入れた！")

# ------------------------------------------------------------
# スクリーンショット
# ------------------------------------------------------------
elif arg1 == "ss":
    # 日付と時刻をファイル名に（例：screenshot_2025-04-24_2113.png）
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    
    # arg2 を優先的に使う、なければ "screenshot"
    base_name = arg2 if arg2 else "screenshot"
    filename = f"{base_name}_{timestamp}.png"

    minescript.screenshot(filename)
    echo(f"📸 スクリーンショットを {filename} に保存しました！")

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    echo(f"未対応のコマンドです: {arg1}")
