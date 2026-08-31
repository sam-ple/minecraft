# ============================================================
# ADVTEST STAGE GENERATOR
# Version : v0.1.00
# Date    : 2026-08-31
#
# Minecraft Java Edition + MineScript
#
# ============================================================
#
# 【目的】
#
#   Advancement Race 用のテストステージを生成する。
#
#   このPythonは「ステージ生成専用」。
#
#   ゲームロジック：
#       → Skript側
#
#   スコア管理：
#       → Skript側
#
#   Advancement判定：
#       → Skript側
#
#   ゲーム開始・終了：
#       → Skript側
#
#   MineScript側では、
#       ・ブロック設置
#       ・エンティティ設置
#       ・チェスト設置
#       ・コマンドブロック設置
#       ・アイテム配布
#       ・ステージ整地
#
#   のみを行う。
#
# ============================================================
#
# 【重要】
#
#   26.2で大量のコマンドを一気に実行すると、
#   どこで問題が発生したのか分かりにくい。
#
#   そのため、このスクリプトは
#
#       ENTER
#          ↓
#       次の工程
#          ↓
#       ENTER
#          ↓
#       次の工程
#
#   という「ステップ実行方式」にしている。
#
#   途中で落ちた場合、
#
#       STEP XX
#
#   の表示から原因箇所を特定できる。
#
# ============================================================
#
# 【操作】
#
#   /advtest
#
#   実行後、
#
#       ENTER
#
#   を押すたびに次のステージ生成工程へ進む。
#
# ============================================================


import minescript as m
import math


# ============================================================
# 基本コマンド
# ============================================================

def cmd(command):
    """
    Minecraftコマンドを1つ実行する。
    """

    m.execute(command)


# ============================================================
# Enter待ち
# ============================================================

def wait_enter(message):
    """
    ユーザーがEnterを押すまで待つ。

    MineScriptの入力待ち機能に依存しないよう、
    Python標準のinput()を使用する。

    ※ターミナル側でEnterを押す。
    """

    print("")
    print("--------------------------------------------------")
    print(message)
    print("ENTER を押すと次へ進みます。")
    print("--------------------------------------------------")

    input()


# ============================================================
# プレイヤー位置
# ============================================================

player = m.player()

px, py, pz = player.position

x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)


# ============================================================
# 相対座標
# ============================================================

def pos(dx=0, dy=0, dz=0):

    return f"{x + dx} {y + dy} {z + dz}"


# ============================================================
# ステップ表示
# ============================================================

STEP = 0


def step_start(title):

    global STEP

    STEP += 1

    print("")
    print("")
    print("==================================================")
    print(f"STEP {STEP}")
    print(title)
    print("==================================================")


def step_complete():

    print("")
    print(f"STEP {STEP} COMPLETE")


# ============================================================
# STEP 1
# 初期設定
# ============================================================

def step_01():

    step_start("初期設定")


    cmd(
        "gamerule spawnMonsters false"
    )

    cmd(
        "difficulty easy"
    )

    cmd(
        "time set night"
    )

    cmd(
        "clear @a"
    )

    cmd(
        "tp @p ~ ~ ~ 180 0"
    )


    step_complete()


# ============================================================
# STEP 2
# 床
# ============================================================

def step_02():

    step_start("床整地")


    cmd(
        f"fill "
        f"{pos(-25,-1,-25)} "
        f"{pos(25,-1,25)} "
        f"minecraft:grass_block"
    )


    step_complete()


# ============================================================
# STEP 3
# 空間クリア
# ============================================================

def step_03():

    step_start("空間クリア")


    cmd(
        f"fill "
        f"{pos(-25,0,-25)} "
        f"{pos(25,9,25)} "
        f"minecraft:air"
    )


    cmd(
        f"fill "
        f"{pos(-25,10,-25)} "
        f"{pos(25,20,25)} "
        f"minecraft:air"
    )


    step_complete()


# ============================================================
# STEP 4
# アーマースタンド
# ============================================================

def step_04():

    step_start("アーマースタンド")


    # --------------------------------------------------------
    # 鉄装備
    # --------------------------------------------------------

    cmd(
        f"summon minecraft:armor_stand "
        f"{pos(-14,0,-5)} "
        f"{{"
        f"ShowArms:true,"
        f"NoGravity:true,"
        f"PersistenceRequired:true,"
        f"equipment:{{"
        f"head:{{id:\"player_head\",Count:1,"
        f"components:{{profile:{{name:\"crocadooo\"}}}}}},"
        f"chest:{{id:\"iron_chestplate\",Count:1}},"
        f"legs:{{id:\"iron_leggings\",Count:1}},"
        f"feet:{{id:\"iron_boots\",Count:1}}"
        f"}}"
        f"}}"
    )


    # --------------------------------------------------------
    # ダイヤ装備
    # --------------------------------------------------------

    cmd(
        f"summon minecraft:armor_stand "
        f"{pos(-13,0,-5)} "
        f"{{"
        f"ShowArms:true,"
        f"NoGravity:true,"
        f"PersistenceRequired:true,"
        f"equipment:{{"
        f"head:{{id:\"wither_skeleton_skull\",Count:1}},"
        f"chest:{{id:\"diamond_chestplate\",Count:1}},"
        f"legs:{{id:\"diamond_leggings\",Count:1}},"
        f"feet:{{id:\"diamond_boots\",Count:1}}"
        f"}}"
        f"}}"
    )


    # --------------------------------------------------------
    # ネザライト装備
    # --------------------------------------------------------

    cmd(
        f"summon minecraft:armor_stand "
        f"{pos(-12,0,-5)} "
        f"{{"
        f"ShowArms:1b,"
        f"NoGravity:1b,"
        f"PersistenceRequired:1b,"
        f"equipment:{{"
        f"head:{{id:\"minecraft:netherite_helmet\",Count:1}},"
        f"chest:{{id:\"minecraft:netherite_chestplate\",Count:1}},"
        f"legs:{{id:\"minecraft:netherite_leggings\",Count:1}},"
        f"feet:{{id:\"minecraft:netherite_boots\",Count:1}}"
        f"}}"
        f"}}"
    )


    step_complete()


# ============================================================
# STEP 5
# ブロック系装飾
# ============================================================

def step_05():

    step_start("作業ブロック・設備")


    # 模様入り本棚
    cmd(
        f"setblock {pos(-10,0,-5)} "
        f"minecraft:chiseled_bookshelf"
    )


    # エンチャントテーブル
    cmd(
        f"setblock {pos(-9,0,-5)} "
        f"minecraft:enchanting_table"
    )


    # 醸造台
    cmd(
        f"setblock {pos(-8,0,-5)} "
        f"minecraft:brewing_stand"
    )


    # 溶鉱炉
    cmd(
        f"setblock {pos(-7,0,-5)} "
        f"minecraft:blast_furnace[facing=south]"
    )


    # 作業台
    cmd(
        f"setblock {pos(0,0,-5)} "
        f"minecraft:crafting_table"
    )


    step_complete()


# ============================================================
# STEP 6
# ダブルチェスト
# ============================================================

def step_06():

    step_start("ダブルチェスト")


    # 左
    cmd(
        f"setblock "
        f"{pos(-6,0,-5)} "
        f"minecraft:chest[facing=south,type=right]"
    )


    # 右
    cmd(
        f"setblock "
        f"{pos(-5,0,-5)} "
        f"minecraft:chest[facing=south,type=left]"
    )


    step_complete()


# ============================================================
# STEP 7
# チェスト中身
# ============================================================

def step_07():

    step_start("チェスト中身")


    cmd(
        f"/data merge block {pos(-6,0,-5)} "
        f"{{Items:["
        f"{{Slot:0b,id:\"minecraft:cobblestone\",Count:64b}},"
        f"{{Slot:1b,id:\"minecraft:iron_ingot\",Count:64b}},"
        f"{{Slot:2b,id:\"minecraft:stone_pickaxe\",Count:1b}},"
        f"{{Slot:3b,id:\"minecraft:shield\",Count:1b}},"
        f"{{Slot:4b,id:\"minecraft:bow\",Count:1b}},"
        f"{{Slot:5b,id:\"minecraft:arrow\",Count:64b}},"
        f"{{Slot:6b,id:\"minecraft:trident\",Count:1b}},"
        f"{{Slot:7b,id:\"minecraft:obsidian\",Count:64b}},"
        f"{{Slot:8b,id:\"minecraft:crying_obsidian\",Count:64b}},"
        f"{{Slot:9b,id:\"minecraft:diamond\",Count:64b}},"
        f"{{Slot:10b,id:\"minecraft:dried_ghast\",Count:1b}},"
        f"{{Slot:11b,id:\"minecraft:sniffer_egg\",Count:1b}},"
        f"{{Slot:12b,id:\"minecraft:wheat_seeds\",Count:64b}},"
        f"{{Slot:13b,id:\"minecraft:blaze_rod\",Count:64b}},"
        f"{{Slot:14b,id:\"minecraft:dragon_egg\",Count:1b}},"
        f"{{Slot:15b,id:\"minecraft:dragon_breath\",Count:64b}},"
        f"{{Slot:16b,id:\"minecraft:elytra\",Count:1b}},"
        f"{{Slot:17b,id:\"minecraft:pumpkin\",Count:64b}}"
        f"]}}"
    )


    step_complete()


# ============================================================
# STEP 8
# ベッド
# ============================================================

def step_08():

    step_start("ベッド")


    cmd(
        f"setblock "
        f"{pos(-4,0,-5)} "
        f"minecraft:red_bed[facing=south,part=foot]"
    )


    cmd(
        f"setblock "
        f"{pos(-4,0,-4)} "
        f"minecraft:red_bed[facing=south,part=head]"
    )


    step_complete()


# ============================================================
# STEP 9
# 村人
# ============================================================

def step_09():

    step_start("村人")


    villager_command = (
        f"summon villager {pos(-3,0,-5)} "
        f"{{"
        f"VillagerData:{{"
        f"level:5,"
        f"profession:\"farmer\","
        f"type:\"plains\""
        f"}},"
        f"Silent:1b,"
        f"Invulnerable:1b,"
        f"NoAI:1b,"
        f"Offers:{{Recipes:["
        f"{{"
        f"buy:{{id:\"emerald\",count:1}},"
        f"sell:{{id:\"snowball\",count:1}},"
        f"maxUses:9999"
        f"}}"
        f"]}}"
        f"}}"
    )


    cmd(villager_command)


    step_complete()


# ============================================================
# STEP 10
# スケルトン
# ============================================================

def step_10():

    step_start("スケルトン")


    cmd(
        f"summon minecraft:skeleton "
        f"{pos(-2,0,-5)} "
        f"{{"
        f"NoAI:1b,"
        f"PersistenceRequired:1b,"
        f"Health:2f,"
        f"Rotation:[0f,0f]"
        f"}}"
    )


    step_complete()


# ============================================================
# STEP 11
# 看板
# ============================================================

def step_11():

    step_start("看板")


    cmd(
        f"setblock "
        f"{pos(-1,0,-5)} "
        f"minecraft:oak_sign[rotation=0]"
    )


    cmd(
        f"/data merge block {pos(-1,0,-5)} "
        f"{{front_text:{{messages:["
        f"\"\","
        f"\"crocadooo\","
        f"\"\","
        f"\"\"]}}}}"
    )


    step_complete()


# ============================================================
# STEP 12
# 動物
# ============================================================

def step_12():

    step_start("動物")


    # --------------------------------------------------------
    # Parrot
    # --------------------------------------------------------

    cmd(
        f"summon minecraft:parrot "
        f"{pos(1,0,-5)} "
        f"{{"
        f"NoAI:1b,"
        f"Silent:1b,"
        f"Rotation:[0f,0f]"
        f"}}"
    )


    # --------------------------------------------------------
    # Armadillo
    # --------------------------------------------------------

    cmd(
        f"summon minecraft:armadillo "
        f"{pos(2,0,-5)} "
        f"{{"
        f"NoAI:1b,"
        f"Silent:1b,"
        f"Rotation:[0f,0f]"
        f"}}"
    )


    # --------------------------------------------------------
    # Allay
    # --------------------------------------------------------

    cmd(
        f"summon minecraft:allay "
        f"{pos(3,0,-5)} "
        f"{{"
        f"Silent:1b,"
        f"NoGravity:1b,"
        f"PersistenceRequired:1b"
        f"}}"
    )


    step_complete()


# ============================================================
# STEP 13
# 金ブロック
# ============================================================

def step_13():

    step_start("金ブロック")


    cmd(
        f"setblock "
        f"{pos(10,-1,-5)} "
        f"minecraft:gold_block"
    )


    step_complete()


# ============================================================
# STEP 14
# 金ブロック用コマンドブロック
# ============================================================

def step_14():

    step_start("金ブロック用コマンドブロック")


    command = (
        f"execute as @a at @s "
        f"if block ~ ~-1 ~ minecraft:gold_block "
        f"run setblock {pos(10,0,-7)} "
        f"minecraft:suspicious_sand"
    )


    command_block = (
        f"setblock {pos(10,-2,-5)} "
        f"minecraft:repeating_command_block"
        f"{{auto:1b,Command:\"{command}\"}}"
    )


    cmd(command_block)


    step_complete()


# ============================================================
# STEP 15
# TP装置
# ============================================================

def step_15():

    step_start("TP装置")


    # --------------------------------------------------------
    # コマンドブロック
    # --------------------------------------------------------

    command = (
        f"tp @p {pos(0,1,0)}"
    )


    cmd(
        f"setblock "
        f"{pos(11,-1,-5)} "
        f"minecraft:command_block"
        f"{{Command:\"{command}\"}}"
    )


    # --------------------------------------------------------
    # 見た目
    # --------------------------------------------------------

    cmd(
        f"setblock "
        f"{pos(11,0,-5)} "
        f"minecraft:stone"
    )


    # --------------------------------------------------------
    # ボタン
    # --------------------------------------------------------

    cmd(
        f"setblock "
        f"{pos(11,0,-4)} "
        f"minecraft:stone_button[facing=south]"
    )


    step_complete()


# ============================================================
# STEP 16
# ダイヤGET看板
# ============================================================

def step_16():

    step_start("クリック看板")


    cmd(
        f"setblock "
        f"{pos(12,0,-5)} "
        f"minecraft:oak_sign"
    )


    # --------------------------------------------------------
    # 看板テキスト
    #
    # クリックイベントはMinecraft側の仕様変更の影響を
    # 受けやすいため、この工程だけ独立させている。
    # --------------------------------------------------------

    sign_command = (
        f'data merge block {pos(12,0,-5)} '
        '{'
        '"front_text":'
        '{'
        '"messages":['
        '"{'
        '\\"text\\":\\"ダイヤGET\\",'
        '\\"clickEvent\\":{'
        '\\"action\\":\\"run_command\\",'
        '\\"value\\":\\"give @s minecraft:diamond 1\\"'
        '}'
        '}",'
        '"",'
        '"",'
        '""'
        ']'
        '}'
        '}'
    )


    cmd(sign_command)


    step_complete()


# ============================================================
# STEP 17
# 水
# ============================================================

def step_17():

    step_start("水")


    cmd(
        f"fill "
        f"{pos(-5,-1,0)} "
        f"{pos(-2,-1,1)} "
        f"minecraft:water"
    )


    step_complete()


# ============================================================
# STEP 18
# 溶岩
# ============================================================

def step_18():

    step_start("溶岩")


    cmd(
        f"fill "
        f"{pos(2,-1,0)} "
        f"{pos(2,-1,1)} "
        f"minecraft:lava"
    )


    step_complete()


# ============================================================
# STEP 19
# 水生生物
# ============================================================

def step_19():

    step_start("水生生物")


    cmd(
        f"summon minecraft:axolotl "
        f"{pos(-3,-1,0)} "
        f"{{NoAI:1b}}"
    )


    cmd(
        f"summon minecraft:tadpole "
        f"{pos(-5,-1,1)} "
        f"{{NoAI:1b}}"
    )


    step_complete()


# ============================================================
# STEP 20
# ネザーゲート枠
# ============================================================

def step_20():

    step_start("ネザーゲート枠")


    BASE_X = 5
    BASE_Y = -1
    BASE_Z = -5


    for dy in range(5):

        for dx in range(4):

            if dx in [0, 3] or dy in [0, 4]:

                block = "minecraft:obsidian"

            else:

                block = "minecraft:air"


            cmd(
                f"setblock "
                f"{pos(BASE_X+dx,BASE_Y+dy,BASE_Z)} "
                f"{block}"
            )


    step_complete()


# ============================================================
# STEP 21
# ネザーゲート点火
# ============================================================

def step_21():

    step_start("ネザーゲート点火")


    cmd(
        f"setblock "
        f"{pos(6,0,-5)} "
        f"minecraft:fire"
    )


    step_complete()


# ============================================================
# STEP 22
# アイテム配布
# ============================================================

def step_22():

    step_start("アイテム配布")


    items = [

        (
            'minecraft:fishing_rod'
            '[enchantments='
            '{"minecraft:luck_of_the_sea":3,'
            '"minecraft:lure":3,'
            '"minecraft:unbreaking":3,'
            '"minecraft:mending":1}] 1'
        ),

        "minecraft:emerald 64",

        "minecraft:bone 64",

        "minecraft:glow_ink_sac 64",

        "minecraft:copper_ingot 64",

        "minecraft:feather 64",

        "minecraft:stick 64",

        "minecraft:suspicious_sand 64",

        "minecraft:compass 1",
    ]


    for item in items:

        cmd(
            f"give @a {item}"
        )


    step_complete()


# ============================================================
# STEP 23
# オオカミ
# ============================================================

def step_23():

    step_start("オオカミ")


    wolf_variants = [

        "pale",
        "woods",
        "ashen",
        "black",
        "chestnut",
        "rusty",
        "spotted",
        "striped",
        "snowy",
        "classic",
        "big",
        "grumpy",

    ]


    base_x = -11
    z_line = -10


    for i, variant in enumerate(wolf_variants):

        cmd(
            f"summon minecraft:wolf "
            f"{pos(base_x+i,0,z_line)} "
            f"{{"
            f"NoAI:1b,"
            f"Sitting:1b,"
            f"Silent:1b,"
            f"CollarColor:14b,"
            f"variant:\"minecraft:{variant}\","
            f"sound_variant:\"minecraft:{variant}\""
            f"}}"
        )


    step_complete()


# ============================================================
# STEP 24
# 骨チェスト
# ============================================================

def step_24():

    step_start("骨チェスト")


    cmd(
        f"setblock "
        f"{pos(-12,0,-10)} "
        f"minecraft:chest[facing=south]"
    )


    cmd(
        f"/data merge block {pos(-12,0,-10)} "
        f"{{Items:["
        f"{{Slot:0b,id:\"minecraft:bone\",Count:64b}},"
        f"{{Slot:1b,id:\"minecraft:bone\",Count:64b}},"
        f"{{Slot:2b,id:\"minecraft:bone\",Count:64b}},"
        f"{{Slot:3b,id:\"minecraft:bone\",Count:64b}},"
        f"{{Slot:4b,id:\"minecraft:bone\",Count:64b}},"
        f"{{Slot:5b,id:\"minecraft:bone\",Count:64b}},"
        f"{{Slot:6b,id:\"minecraft:bone\",Count:64b}},"
        f"{{Slot:7b,id:\"minecraft:bone\",Count:64b}}"
        f"]}}"
    )


    step_complete()


# ============================================================
# STEP 25
# 猫
# ============================================================

def step_25():

    step_start("猫")


    cat_variants = [

        "tabby",
        "black",
        "red",
        "siamese",
        "british_shorthair",
        "calico",
        "persian",
        "ragdoll",
        "white",
        "jellie",
        "all_black",

    ]


    base_x = -11
    z_line = -14


    for i, variant in enumerate(cat_variants):

        cmd(
            f"summon minecraft:cat "
            f"{pos(base_x+i,0,z_line)} "
            f"{{"
            f"NoAI:1b,"
            f"Sitting:1b,"
            f"Silent:1b,"
            f"variant:\"minecraft:{variant}\""
            f"}}"
        )


    step_complete()


# ============================================================
# STEP 26
# 魚チェスト
# ============================================================

def step_26():

    step_start("魚チェスト")


    cmd(
        f"setblock "
        f"{pos(-12,0,-14)} "
        f"minecraft:chest[facing=south]"
    )


    cmd(
        f"/data merge block {pos(-12,0,-14)} "
        f"{{Items:["
        f"{{Slot:0b,id:\"minecraft:cod\",Count:64b}},"
        f"{{Slot:1b,id:\"minecraft:cod\",Count:64b}},"
        f"{{Slot:2b,id:\"minecraft:salmon\",Count:64b}},"
        f"{{Slot:3b,id:\"minecraft:salmon\",Count:64b}}"
        f"]}}"
    )


    step_complete()


# ============================================================
# STEP 27
# カエル
# ============================================================

def step_27():

    step_start("カエル")


    frog_variants = [

        "temperate",
        "warm",
        "cold",

    ]


    base_x = -11
    z_line = -18


    for i, variant in enumerate(frog_variants):

        cmd(
            f"summon minecraft:frog "
            f"{pos(base_x+i,0,z_line)} "
            f"{{"
            f"NoAI:1b,"
            f"Silent:1b,"
            f"variant:\"minecraft:{variant}\""
            f"}}"
        )


    step_complete()


# ============================================================
# STEP 28
# リードチェスト
# ============================================================

def step_28():

    step_start("リードチェスト")


    cmd(
        f"setblock "
        f"{pos(-12,0,-18)} "
        f"minecraft:chest[facing=south]"
    )


    cmd(
        f"/data merge block {pos(-12,0,-18)} "
        f"{{Items:["
        f"{{Slot:0b,id:\"minecraft:lead\",Count:64b}},"
        f"{{Slot:1b,id:\"minecraft:lead\",Count:64b}},"
        f"{{Slot:2b,id:\"minecraft:lead\",Count:64b}}"
        f"]}}"
    )


    step_complete()


# ============================================================
# STEP 29
# 完了
# ============================================================

def step_29():

    step_start("ステージ生成完了")


    m.echo(
        "=============================================="
    )

    m.echo(
        "ADVTEST STAGE COMPLETED"
    )

    m.echo(
        "MineScript : STAGE ONLY"
    )

    m.echo(
        "Game Logic : Skript"
    )

    m.echo(
        "=============================================="
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("")
    print("")
    print("==================================================")
    print(" ADVTEST STAGE GENERATOR")
    print(" Minecraft 26.2")
    print("==================================================")
    print("")
    print("ENTER を押すたびに1工程ずつ進みます。")
    print("途中で問題が発生した場合はSTEP番号を確認してください。")
    print("")


    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    wait_enter(
        "STEP 1 : 初期設定を開始します。"
    )

    step_01()


    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    wait_enter(
        "STEP 2 : 床整地を開始します。"
    )

    step_02()


    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    wait_enter(
        "STEP 3 : 空間クリアを開始します。"
    )

    step_03()


    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    wait_enter(
        "STEP 4 : アーマースタンドを設置します。"
    )

    step_04()


    # --------------------------------------------------------
    # STEP 5
    # --------------------------------------------------------

    wait_enter(
        "STEP 5 : 作業ブロックを設置します。"
    )

    step_05()


    # --------------------------------------------------------
    # STEP 6
    # --------------------------------------------------------

    wait_enter(
        "STEP 6 : ダブルチェストを設置します。"
    )

    step_06()


    # --------------------------------------------------------
    # STEP 7
    # --------------------------------------------------------

    wait_enter(
        "STEP 7 : チェストの中身を設定します。"
    )

    step_07()


    # --------------------------------------------------------
    # STEP 8
    # --------------------------------------------------------

    wait_enter(
        "STEP 8 : ベッドを設置します。"
    )

    step_08()


    # --------------------------------------------------------
    # STEP 9
    # --------------------------------------------------------

    wait_enter(
        "STEP 9 : 村人を設置します。"
    )

    step_09()


    # --------------------------------------------------------
    # STEP 10
    # --------------------------------------------------------

    wait_enter(
        "STEP 10 : スケルトンを設置します。"
    )

    step_10()


    # --------------------------------------------------------
    # STEP 11
    # --------------------------------------------------------

    wait_enter(
        "STEP 11 : 看板を設置します。"
    )

    step_11()


    # --------------------------------------------------------
    # STEP 12
    # --------------------------------------------------------

    wait_enter(
        "STEP 12 : 動物を設置します。"
    )

    step_12()


    # --------------------------------------------------------
    # STEP 13
    # --------------------------------------------------------

    wait_enter(
        "STEP 13 : 金ブロックを設置します。"
    )

    step_13()


    # --------------------------------------------------------
    # STEP 14
    # --------------------------------------------------------

    wait_enter(
        "STEP 14 : 金ブロック用コマンドブロックを設置します。"
    )

    step_14()


    # --------------------------------------------------------
    # STEP 15
    # --------------------------------------------------------

    wait_enter(
        "STEP 15 : TP装置を設置します。"
    )

    step_15()


    # --------------------------------------------------------
    # STEP 16
    # --------------------------------------------------------

    wait_enter(
        "STEP 16 : クリック看板を設置します。"
    )

    step_16()


    # --------------------------------------------------------
    # STEP 17
    # --------------------------------------------------------

    wait_enter(
        "STEP 17 : 水を設置します。"
    )

    step_17()


    # --------------------------------------------------------
    # STEP 18
    # --------------------------------------------------------

    wait_enter(
        "STEP 18 : 溶岩を設置します。"
    )

    step_18()


    # --------------------------------------------------------
    # STEP 19
    # --------------------------------------------------------

    wait_enter(
        "STEP 19 : 水生生物を設置します。"
    )

    step_19()


    # --------------------------------------------------------
    # STEP 20
    # --------------------------------------------------------

    wait_enter(
        "STEP 20 : ネザーゲート枠を設置します。"
    )

    step_20()


    # --------------------------------------------------------
    # STEP 21
    # --------------------------------------------------------

    wait_enter(
        "STEP 21 : ネザーゲートを点火します。"
    )

    step_21()


    # --------------------------------------------------------
    # STEP 22
    # --------------------------------------------------------

    wait_enter(
        "STEP 22 : アイテムを配布します。"
    )

    step_22()


    # --------------------------------------------------------
    # STEP 23
    # --------------------------------------------------------

    wait_enter(
        "STEP 23 : オオカミを設置します。"
    )

    step_23()


    # --------------------------------------------------------
    # STEP 24
    # --------------------------------------------------------

    wait_enter(
        "STEP 24 : 骨チェストを設置します。"
    )

    step_24()


    # --------------------------------------------------------
    # STEP 25
    # --------------------------------------------------------

    wait_enter(
        "STEP 25 : 猫を設置します。"
    )

    step_25()


    # --------------------------------------------------------
    # STEP 26
    # --------------------------------------------------------

    wait_enter(
        "STEP 26 : 魚チェストを設置します。"
    )

    step_26()


    # --------------------------------------------------------
    # STEP 27
    # --------------------------------------------------------

    wait_enter(
        "STEP 27 : カエルを設置します。"
    )

    step_27()


    # --------------------------------------------------------
    # STEP 28
    # --------------------------------------------------------

    wait_enter(
        "STEP 28 : リードチェストを設置します。"
    )

    step_28()


    # --------------------------------------------------------
    # STEP 29
    # --------------------------------------------------------

    step_29()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()