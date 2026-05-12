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
    "sunrise": "sunrise",
    "day": "day",
    "noon": "noon",
    "sunset": "sunset",
    "night": "night",
    "midnight": "midnight",
}

map_weather = {
    "clear": "clear",
    "rain": "rain",
    "thunder": "thunder",
}

map_gamemode = {
    "survival": "survival",
    "creative": "creative",
    "spectator": "spectator",
    "adventure": "adventure",
}

# 方角マッピング（東西南北のY軸回転値）
map_direction = {
    "north": 180,
    "south": 0,
    "east": -90,
    "west": 90
}

# ------------------------------------------------------------
# ヘルプ
# ------------------------------------------------------------
if user_input == "help":
    text_help = """
=== 利用できるコマンド一覧 ===
【時間変更】
  sunrise / day / noon / sunset / night / midnight … 時間を変更

【天気変更】
  clear / rain / thunder … 天気を変更

【ゲームモード】
  survival / creative / spectator / adventure … モード変更

【向き変更】
  north / south / east / west

【便利コマンド】
  test … テスト用
  action … クリックアクション
  start … カウントダウンして開始
  end  … 終了
  where … プレイヤーの現在位置を表示
  timer … 1分タイマーを開始
  biome … 最寄りのバイオーム座標をまとめて表示
  fireworks … 花火を打ち上げる
  mode … 配信用設定（昼固定・モブ湧きオフなど）
  dot_chicken … ニワトリのドット絵を空に書く
  cleardot … ドット絵を削除
  sheep_pink … ピンクの羊を召喚
  animals … 周囲に動物たちを召喚
  crafttable … 作業台を渡す
  clearitem … インベントリ全削除
  dropper … アイテム入りのドロッパーを設置
  cheatpack … チート装備一式（ダイヤ＆食べ物）
  nethergate … ネザーゲートを作成
  bed … ベッドを設置
  base_kit … 作業台・かまど・チェストセットを設置
  house … 家を作成
  fishrod … 最強の釣り竿を渡す
  flatten … 足元を整地
  lake … 湖を生成
  grass … 足元を草ブロックにする
  damage_grass … 草の上でダメージ受ける
  nodamage_grass … ダメージ設定を解除
  count … ジャンプをカウント
  resetcount … ジャンプのカウントをリセット
  nocount … ジャンプのカウントを解除
  
【ミニゲーム】
  fishing … 魚釣り
  archery … 的当て
  slot … スロット
  panelrush … パネルラッシュ
  mobhunt … モブハント
  timeattack … タイムアタック  

※コマンド例: `\run fishrod`
"""
    minescript.echo(text_help)

# ------------------------------------------------------------ 
# テスト
# ------------------------------------------------------------ 
elif user_input in test:
    text_test = """
        /say テストメッセージが表示されました！
        /time set day
        /weather clear
    """
    # 各コマンドを実行
    for command in text_test.strip().split('\n'):
        minescript.execute(command)

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
# スタート
# ------------------------------------------------------------
elif user_input == "start":
    # 3
    minescript.execute('/title @a title {"text":"3","color":"red","bold":true}')
    time.sleep(1)

    # 2
    minescript.execute('/title @a title {"text":"2","color":"gold","bold":true}')
    time.sleep(1)

    # 1
    minescript.execute('/title @a title {"text":"1","color":"yellow","bold":true}')
    time.sleep(1)

    # スタート！
    minescript.execute('/title @a title {"text":"スタート！","color":"green","bold":true}')
    minescript.echo("スタートしました！")

# ------------------------------------------------------------ 
# 画面を真っ暗にするエンド効果
# ------------------------------------------------------------
elif user_input == "end":
    minescript.execute('/title @a title {"text":"終了","color":"dark_red","bold":true}')
    minescript.execute('/effect give @a minecraft:blindness 10 1 true')
    minescript.echo("終了...")

# # ------------------------------------------------------------  
# # クリックでアクション 
# # ------------------------------------------------------------
# elif user_input == "action":
#     minescript.execute('/title @a title {"text":"クリックでアクション","color":"yellow","bold":true}')

#     minescript.execute('''
#         /tellraw @a {
#         "text": ">> ここをクリックして挨拶する！",
#         "color": "gold",
#         "bold": true,
#         "clickEvent": {
#             "action": "run_command",
#             "value": "/say こんにちは！"
#         },
#         "hoverEvent": {
#             "action": "show_text",
#             "contents": "クリックで「こんにちは！」と表示"
#         }
#         }
#     ''')

# ------------------------------------------------------------
# 配信用設定
# ------------------------------------------------------------
elif user_input == "mode":
    minescript.execute('/title @a title {"text":"配信用設定","color":"yellow","bold":true}')
    map_settings = {
        "keepInventory": "true",
        "doDaylightCycle": "false",
        "doMobSpawning": "false",
        "showCoordinates": "true",  # 座標表示をオンに追加！
    }
    for rule, value in map_settings.items():
        minescript.execute(f"/gamerule {rule} {value}")
    minescript.execute("/time set day")      # 時間を昼に
    minescript.execute("/weather clear")     # 天気を晴れに
    minescript.echo("「配信用設定」を適用しました！（キープインベントリ＋常に昼＋モブ湧きオフ＋座標表示）")

# ------------------------------------------------------------
# インベントリ全削除
# ------------------------------------------------------------
elif user_input == "clearitem":
    minescript.execute('/title @a title {"text":"インベントリ全削除","color":"yellow","bold":true}')
    minescript.execute('/clear @p')
    minescript.echo("インベントリをすべて削除しました。")

# # ------------------------------------------------------------
# # 整地
# # ------------------------------------------------------------
# elif user_input == "flatten":
#     minescript.execute('/title @a title {"text":"整地","color":"yellow","bold":true}')
#     x, y, z = minescript.player_position()
#     # プレイヤーの向きを取得
#     yaw = minescript.player_rotation()[0]  # yaw（向いている方向）の取得
    
#     # 向いている方向に応じて整地範囲を調整
#     # ここでは簡単な例として、+Z方向を前方に向けて、向いている方向に整地を行う
#     if -45 <= yaw < 45:  # 北方向
#         direction = (0, 0)
#     elif 45 <= yaw < 135:  # 東方向
#         direction = (1, 0)
#     elif 135 <= yaw < 225:  # 南方向
#         direction = (0, 1)
#     else:  # 西方向
#         direction = (-1, 0)
    
#     # プレイヤーの周囲を整地
#     for dx in range(-5, 6):
#         for dz in range(-5, 6):
#             # 向いている方向に合わせてブロックを削除
#             new_x = x + dx * direction[0]
#             new_z = z + dz * direction[1]
#             # /setblock を使用
#             minescript.execute(f"/setblock {new_x} {y - 1} {new_z} minecraft:air")
    
#     minescript.echo("整地が完了しました。")


# ------------------------------------------------------------
# 作業台
# ------------------------------------------------------------
elif user_input == "crafttable":
    minescript.execute('/title @a title {"text":"作業台を渡す","color":"yellow","bold":true}')
    minescript.execute('/give @p minecraft:crafting_table 1')
    minescript.echo("作業台を渡しました。")

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

# # ------------------------------------------------------------
# # 湖を作成
# # ------------------------------------------------------------
# elif user_input == "lake":
#     minescript.execute('/title @a title {"text":"湖を作成","color":"yellow","bold":true}')
#     # プレイヤーの現在位置を取得
#     x, y, z = minescript.player_position()
#     x, y, z = int(x), int(y), int(z)

#     # 湖のサイズ
#     width = 5
#     depth = 1
#     length = 6

#     # ブロック配置
#     for dx in range(-width // 2, width // 2 + 1):
#         for dz in range(0, length):
#             # 水を置く（地面を掘って水で埋める）
#             minescript.execute(f"setblock {x + dx} {y - depth} {z + dz} minecraft:water")
#             # 水の下は土
#             minescript.execute(f"setblock {x + dx} {y - depth - 1} {z + dz} minecraft:dirt")
#             # 周囲に囲いブロック（草ブロック）を追加して湖っぽく
#             minescript.execute(f"setblock {x + dx} {y - depth} {z + dz + 1} minecraft:grass_block")
#             minescript.execute(f"setblock {x + dx} {y - depth} {z + dz - 1} minecraft:grass_block")

#     minescript.echo("囲い付きの湖を生成しました。")

# ------------------------------------------------------------
# チート装備一式（ダイヤ装備＆自動装備＆食べ物64個）
# ------------------------------------------------------------
elif user_input == "cheatpack":
    minescript.execute('/title @a title {"text":"チート装備一式を渡す","color":"yellow","bold":true}')
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

    minescript.echo("チート装備を配布しました。")

# # ------------------------------------------------------------
# # 家を作成
# # ------------------------------------------------------------
# elif user_input == "house":
#     minescript.execute('/title @a title {"text":"木の家を作成中","color":"yellow","bold":true}')
#     x, y, z = map(int, minescript.player_position())
    
#     width = 5
#     height = 4
#     floor_block = "oak_planks"
#     wall_block = "oak_planks"
#     carpet_block = "white_carpet"
#     window_block = "glass_pane"
#     roof_block = "spruce_planks"
#     light_block = "lantern"

#     # 壁・天井・床
#     for dx in range(-width//2, width//2 + 1):
#         for dy in range(0, height + 1):
#             for dz in range(-width//2, width//2 + 1):
#                 bx, by, bz = x + dx, y + dy, z + dz

#                 # 床
#                 if dy == 0:
#                     minescript.execute(f"setblock {bx} {by} {bz} {floor_block}")
#                     minescript.execute(f"setblock {bx} {by+1} {bz} {carpet_block}")

#                 # 壁
#                 elif dx in [-width//2, width//2] or dz in [-width//2, width//2]:
#                     # 窓
#                     if dy == 2 and (dx in [-width//2, width//2] or dz in [-width//2, width//2]):
#                         minescript.execute(f"setblock {bx} {by} {bz} {window_block}")
#                     else:
#                         minescript.execute(f"setblock {bx} {by} {bz} {wall_block}")

#                 # 天井
#                 elif dy == height:
#                     minescript.execute(f"setblock {bx} {by} {bz} {roof_block}")
#                 else:
#                     # 内部は空洞
#                     minescript.execute(f"setblock {bx} {by} {bz} air")

#     # ドア設置（正面中央）
#     minescript.execute(f"setblock {x} {y+1} {z - width//2} oak_door[facing=south,half=lower]")
#     minescript.execute(f"setblock {x} {y+2} {z - width//2} oak_door[facing=south,half=upper]")

#     # 内装（ベッド・チェスト・作業台）
#     minescript.execute(f"setblock {x - 1} {y+1} {z} white_bed")
#     minescript.execute(f"setblock {x + 1} {y+1} {z} chest")
#     minescript.execute(f"setblock {x} {y+1} {z} crafting_table")

#     # ランタン設置（天井中央）
#     minescript.execute(f"setblock {x} {y + height} {z} air")  # 一旦空気
#     minescript.execute(f"setblock {x} {y + height - 1} {z} {light_block} hanging=true")

#     minescript.echo("🏡 ウッディな家が完成しました！")


# ------------------------------------------------------------
# ピンクの羊を召喚
# ------------------------------------------------------------
elif user_input == "sheep_pink":
    minescript.execute('/title @a title {"text":"ピンクの羊を召喚","color":"yellow","bold":true}')
    
    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()
    
    # 召喚位置を調整
    summon_x = x + 5  # x座標を5ブロック前に
    summon_y = y  # 高さはそのまま
    summon_z = z  # z座標はそのまま

    # ピンクの羊を召喚
    minescript.execute(f'/summon minecraft:sheep {summon_x} {summon_y} {summon_z} {{Color:6}}')

    minescript.echo("ピンクの羊を召喚しました。")

# ------------------------------------------------------------ 
# 周囲にフレンドリーな動物を召喚
# ------------------------------------------------------------ 
elif user_input == "animals":
    minescript.execute('/title @a title {"text":"フレンドリーMOB召喚！","color":"light_purple","bold":true}')
    
    # プレイヤーの位置を取得
    x, y, z = minescript.player_position()

    # 各Mobとオフセットのリスト（Mob名, Xオフセット, Zオフセット, NBT）
    mob_list = [
        ("sheep", 5, 0, "{Color:6}"),  # ピンクの羊（Color:6）
        ("allay", -5, 0, "{}"),        # アレイ
        ("cow", 0, 5, "{}"),
        ("chicken", 0, -5, "{}"),
        ("parrot", 3, 3, "{}"),
        ("fox", -3, -3, "{Type:\"red\"}"),  # 赤キツネ
        ("rabbit", 4, -2, "{}")
    ]

    # 各Mobをスポーン
    for mob, dx, dz, nbt in mob_list:
        sx = x + dx
        sz = z + dz
        minescript.execute(f'/summon minecraft:{mob} {sx} {y} {sz} {nbt}')

    minescript.echo("友好的な動物たちを召喚しました！")

# # ------------------------------------------------------------
# # タイマー
# # ------------------------------------------------------------
# elif user_input == "timer":
#     minescript.execute('/title @a title {"text":"タイマーを作成","color":"yellow","bold":true}')
#     # ボスバー作成（存在しない場合はエラー回避）
#     minescript.execute('/bossbar add timer.timer "残り時間"')
#     minescript.execute('/bossbar set timer.timer players @a')
#     minescript.execute('/bossbar set timer.timer max 60')  # 1分（60秒）
#     minescript.execute('/bossbar set timer.timer value 60')
#     minescript.echo("1分タイマーを開始します")

#     # 非同期で1秒ごとに減少
#     for i in range(60, 0, -1):
#         minescript.execute(f"/bossbar set timer.timer value {i}")
#         minescript.execute(f"/title @a actionbar [{i}秒]")
#         # 1秒待機して次の更新
#         minescript.execute(f"/schedule function mynamespace:timer_update {i}t")

#     # タイマー終了後
#     minescript.execute('/bossbar remove timer.timer')
#     minescript.echo("タイマー終了！")

# ------------------------------------------------------------
# 周辺を草ブロックに変更
# ------------------------------------------------------------
elif user_input == "grass":
    minescript.execute('/title @a title {"text":"周辺を草ブロックに変更","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z)

    radius = 2  # 周囲2ブロック → 5x5の範囲になる

    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            minescript.execute(f"setblock {x + dx} {y - 1} {z + dz} minecraft:grass_block")

    minescript.echo("足元と周囲を草ブロックに変えたよ🌱")

# # ------------------------------------------------------------
# # プレイヤーが草ブロックの上にいるときにダメージを与える
# # ------------------------------------------------------------
# elif user_input == "damage_grass":
#     minescript.execute('/title @a title {"text":"草ブロックでダメージを受ける","color":"yellow","bold":true}')
#     # プレイヤーが移動して草ブロックにいる場合にもダメージを与える
#     while True:
#         minescript.execute('/execute as @a at @s if block ~ ~-1 ~ minecraft:grass_block run damage @s 1')  # 1ダメージ
#     minescript.echo("草ブロックの上でダメージを受ける設定を有効にしました。")

# # ------------------------------------------------------------
# # プレイヤーが草ブロックの上でダメージを受けないように設定を解除
# # ------------------------------------------------------------
# elif user_input == "nodamage_grass":
#     minescript.execute('/title @a title {"text":"ダメージ解除","color":"yellow","bold":true}')
#     # プレイヤーが草ブロックの上でダメージを受けないように
#     minescript.execute('/execute as @a at @s if block ~ ~-1 ~ minecraft:grass_block run effect clear @s minecraft:instant_damage') 
#     minescript.echo("草ブロックの上でダメージを受ける設定を解除しました。")

# ------------------------------------------------------------ 
# プレイヤーがジャンプした回数をカウント 
# ------------------------------------------------------------ 
elif user_input == "count":
    minescript.execute('/title @a title {"text":"カウント開始","color":"yellow","bold":true}')
    # もしまだ目的が設定されていない場合にのみ設定
    minescript.execute('/scoreboard objectives add Jump minecraft.custom:minecraft.jump "ジャンプした回数"')
    minescript.echo("ジャンプをカウントします。")

# ------------------------------------------------------------ 
# ジャンプした回数のカウントをリセット
# ------------------------------------------------------------ 
elif user_input == "resetcount":
    minescript.execute('/title @a title {"text":"カウントリセット","color":"yellow","bold":true}')
    # リセット用にスコアを0にする
    minescript.execute('/scoreboard players set @a Jump 0')
    minescript.echo("ジャンプのカウントをリセットしました。")

# ------------------------------------------------------------ 
# ジャンプした回数のカウントを解除
# ------------------------------------------------------------ 
elif user_input == "nocount":
    minescript.execute('/title @a title {"text":"カウント解除","color":"yellow","bold":true}')
    # カウントを解除
    minescript.execute('/scoreboard objectives remove Jump')
    minescript.echo("ジャンプのカウントを解除しました。")

# ------------------------------------------------------------
# ドット絵（ニワトリ）
# ------------------------------------------------------------
elif user_input == "dot_chicken":
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
# シンプルなドロッパー装置を設置（横にボタン、中にアイテム）
# ------------------------------------------------------------
elif user_input == "dropper":
    minescript.execute('/title @a title {"text":"ドロッパー装置を設置","color":"gold","bold":true}')

    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z + 3)  # プレイヤーの前方に設置

    # ドロッパーをプレイヤーに向けて設置（南向き）
    minescript.execute(f"/setblock {x} {y} {z} minecraft:dropper[facing=south]")

    # 側面（東側）にボタン設置
    minescript.execute(f"/setblock {x + 1} {y} {z} minecraft:stone_button[facing=west]")

    # ランダムなアイテムを複数スロットに入れる（CommandでNBT操作）
    items = [
        {"id": "diamond", "Count": 1},
        {"id": "arrow", "Count": 8},
        {"id": "apple", "Count": 2},
        {"id": "cooked_beef", "Count": 4},
        {"id": "iron_ingot", "Count": 3},
    ]

    # NBT形式に変換
    nbt_items = ",".join([
        f'{{Slot:{i}b,id:"minecraft:{item["id"]}",Count:{item["Count"]}b}}'
        for i, item in enumerate(items)
    ])

    # ドロッパーにアイテムをセット
    minescript.execute(f"/data merge block {x} {y} {z} {{Items:[{nbt_items}]}}")

    minescript.echo("ボタン付きドロッパーを設置したよ！🎁")
    
# ------------------------------------------------------------
# 花火を打ち上げる
# ------------------------------------------------------------
elif user_input == "fireworks":
    minescript.execute('/title @a title {"text":"花火を打ち上げる","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y + 2), int(z)  # プレイヤーの少し上

    minescript.execute(f"summon firework_rocket {x} {y} {z} {{LifeTime:20}}")
    minescript.echo("花火を打ち上げたよ！🎆")

# ------------------------------------------------------------
# ベッドを設置
# ------------------------------------------------------------
elif user_input == "bed":
    minescript.execute('/title @a title {"text":"ベッドを設置","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z + 1)

    # ベッドの足側（南向きに設置）
    minescript.execute(f"setblock {x} {y} {z} minecraft:red_bed[facing=south,part=foot]")
    # ベッドの頭側
    minescript.execute(f"setblock {x} {y} {z + 1} minecraft:red_bed[facing=south,part=head]")

    minescript.echo("仮拠点に赤いベッドを置いたよ🛏️")

# ------------------------------------------------------------
# 簡易な作業台・かまど・チェストセットを配置
# ------------------------------------------------------------
elif user_input == "base_kit":
    minescript.execute('/title @a title {"text":"ベースキットを設置","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z + 2)

    # 並べて設置
    minescript.execute(f"setblock {x} {y} {z} minecraft:crafting_table")
    minescript.execute(f"setblock {x + 1} {y} {z} minecraft:furnace")
    minescript.execute(f"setblock {x + 2} {y} {z} minecraft:chest")

    minescript.echo("作業キットを設置したよ🔧")

# ------------------------------------------------------------
# プレイヤーの現在位置を表示
# ------------------------------------------------------------
elif user_input == "where":
    minescript.execute('/title @a title {"text":"プレイヤーの現在位置","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    minescript.echo(f"現在位置: X={int(x)}, Y={int(y)}, Z={int(z)}")

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
    minescript.execute('/title @a title {"text":"バイオーム座標を取得","color":"yellow","bold":true}')
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z)

    map_biomes = ["desert", "forest", "taiga", "swamp", "plains"]
    results = {}
    
    for biome in map_biomes:
        result = minescript.execute(f'/locate biome {biome}')
        results[biome] = result
    
    # 結果を表示
    for biome, location in results.items():
        minescript.echo(f"最寄りの{biome}バイオームの座標: {location}")

# ------------------------------------------------------------ 
# ネザーゲートを生成＆着火
# ------------------------------------------------------------ 
elif user_input == "nethergate":
    minescript.execute('/title @a title {"text":"ネザーゲートを設置","color":"red","bold":true}')
    
    x, y, z = minescript.player_position()
    x, y, z = int(x), int(y), int(z + 3)  # プレイヤーの前方に設置

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

    minescript.echo("ネザーゲートを作成・起動したよ！🌌🔥")

# ------------------------------------------------------------
# 未対応
# ------------------------------------------------------------
else:
    minescript.echo(f"未対応のコマンドです: {user_input}")