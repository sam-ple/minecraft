import minescript as m
import math
import queue

# ============================================================
# ADVANCEMENT TEST STAGE GENERATOR
# Version : v0.1.00
#
# Minecraft Java Edition 26.2
# Minescript
#
# ============================================================
#
# 【目的】
#
#   Skriptで作成するゲーム本体のための
#   「テストステージ」を生成する専用Minescript。
#
#   Minescript
#       ↓
#   ステージ生成のみ
#
#   Skript
#       ↓
#   ゲームシステム
#
# ------------------------------------------------------------
#
# 【操作】
#
#   \advtest
#       ステージ生成開始
#
#   Enter
#       次のSTEPへ進む
#
#   ESC
#       ステージ生成を中断
#
# ------------------------------------------------------------
#
# 【重要】
#
#   このスクリプトにはゲームロジックを入れない。
#
#   ・スコア
#   ・プレイヤー管理
#   ・アドバンスメント判定
#   ・死亡処理
#   ・ゲーム開始
#   ・ゲーム終了
#
#   これらはすべてSkript側で担当する。
#
# ------------------------------------------------------------
#
# 【26.2対応】
#
#   Minecraft 1.20.5以降のItem Stack形式変更に合わせ、
#   Count ではなく count を使用。
#
#   例：
#
#       {id:"minecraft:diamond",count:1}
#
# ============================================================


# ============================================================
# 基本設定
# ============================================================

SCRIPT_NAME = "ADVTEST"

# Enterキー
# GLFW_KEY_ENTER = 257
KEY_ENTER = 257

# Escapeキー
# GLFW_KEY_ESCAPE = 256
KEY_ESCAPE = 256


# ============================================================
# コマンド実行
# ============================================================

def cmd(command):
    """
    Minecraftコマンドを1個実行する。

    重要：
    ここでは大量のコマンドを連続で投げず、
    STEP単位で少しずつ実行する。
    """
    m.execute(command)


# ============================================================
# チャット表示
# ============================================================

def msg(text):
    """
    自分だけに表示されるメッセージ。
    """
    m.echo(text)


def separator():
    msg("----------------------------------------")


def step_start(step_no, title):
    """
    STEP開始表示。
    """

    separator()
    msg(f"[{SCRIPT_NAME}] STEP {step_no:02d}")
    msg(f"内容 : {title}")
    separator()


def step_action(step_no, action_no, text):
    """
    STEP内部の進捗表示。
    """

    msg(f"[{step_no:02d}-{action_no:02d}] {text}")


def step_complete(step_no):
    """
    STEP完了表示。
    """

    separator()
    msg(f"[{SCRIPT_NAME}] STEP {step_no:02d} COMPLETE")
    msg("Enter : 次のSTEP")
    msg("ESC   : 中断")
    separator()


def step_error(step_no, action_no, text):
    """
    エラー表示。

    Python側で例外が発生した場合に使用。
    """

    separator()
    msg(f"[{SCRIPT_NAME}] ERROR")
    msg(f"STEP   : {step_no:02d}")
    msg(f"ACTION : {action_no:02d}")
    msg(f"内容   : {text}")
    separator()


# ============================================================
# プレイヤー位置
# ============================================================

p = m.player()

px, py, pz = p.position

x = math.floor(px)
y = math.floor(py)
z = math.floor(pz)


# ============================================================
# 相対座標 → 絶対座標
# ============================================================

def pos(dx=0, dy=0, dz=0):
    return f"{x + dx} {y + dy} {z + dz}"


# ============================================================
# STEP 01
# 初期設定
# ============================================================

def step01():

    step_no = 1
    action = 0

    step_start(step_no, "初期設定")

    action += 1
    step_action(step_no, action, "モンスター生成OFF")
    cmd("gamerule spawnMonsters false")

    action += 1
    step_action(step_no, action, "難易度 EASY")
    cmd("difficulty easy")

    action += 1
    step_action(step_no, action, "時間を夜に設定")
    cmd("time set night")

    action += 1
    step_action(step_no, action, "全プレイヤーのインベントリをクリア")
    cmd("clear @a")

    action += 1
    step_action(step_no, action, "プレイヤーの向きを北へ設定")
    cmd("tp @p ~ ~ ~ 180 0")

    step_complete(step_no)


# ============================================================
# STEP 02
# 床・空間
# ============================================================

def step02():

    step_no = 2
    action = 0

    step_start(step_no, "床・空間生成")

    action += 1
    step_action(step_no, action, "床を草ブロックに変更")

    cmd(
        f"fill "
        f"{pos(-25, -1, -25)} "
        f"{pos(25, -1, 25)} "
        f"minecraft:grass_block"
    )

    action += 1
    step_action(step_no, action, "地上空間をクリア")

    cmd(
        f"fill "
        f"{pos(-25, 0, -25)} "
        f"{pos(25, 9, 25)} "
        f"minecraft:air"
    )

    action += 1
    step_action(step_no, action, "上空をクリア")

    cmd(
        f"fill "
        f"{pos(-25, 10, -25)} "
        f"{pos(25, 20, 25)} "
        f"minecraft:air"
    )

    step_complete(step_no)


# ============================================================
# STEP 03
# Armor Stand
# ============================================================

def step03():

    step_no = 3
    action = 0

    step_start(step_no, "Armor Stand 3体")

    # --------------------------------------------------------
    # Iron
    # --------------------------------------------------------

    action += 1
    step_action(step_no, action, "鉄装備Armor Stand")

    cmd(
        f'summon minecraft:armor_stand {pos(-14,0,-5)} '
        f'{{'
        f'ShowArms:true,'
        f'NoGravity:true,'
        f'PersistenceRequired:true,'
        f'equipment:{{'
        f'head:{{id:"minecraft:player_head",count:1,'
        f'components:{{profile:{{name:"crocadooo"}}}}}},'
        f'chest:{{id:"minecraft:iron_chestplate",count:1}},'
        f'legs:{{id:"minecraft:iron_leggings",count:1}},'
        f'feet:{{id:"minecraft:iron_boots",count:1}}'
        f'}}'
        f'}}'
    )

    # --------------------------------------------------------
    # Diamond
    # --------------------------------------------------------

    action += 1
    step_action(step_no, action, "ダイヤ装備Armor Stand")

    cmd(
        f'summon minecraft:armor_stand {pos(-13,0,-5)} '
        f'{{'
        f'ShowArms:true,'
        f'NoGravity:true,'
        f'PersistenceRequired:true,'
        f'equipment:{{'
        f'head:{{id:"minecraft:wither_skeleton_skull",count:1}},'
        f'chest:{{id:"minecraft:diamond_chestplate",count:1}},'
        f'legs:{{id:"minecraft:diamond_leggings",count:1}},'
        f'feet:{{id:"minecraft:diamond_boots",count:1}}'
        f'}}'
        f'}}'
    )

    # --------------------------------------------------------
    # Netherite
    # --------------------------------------------------------

    action += 1
    step_action(step_no, action, "ネザライト装備Armor Stand")

    cmd(
        f'summon minecraft:armor_stand {pos(-12,0,-5)} '
        f'{{'
        f'ShowArms:1b,'
        f'NoGravity:1b,'
        f'PersistenceRequired:1b,'
        f'equipment:{{'
        f'head:{{id:"minecraft:netherite_helmet",count:1}},'
        f'chest:{{id:"minecraft:netherite_chestplate",count:1}},'
        f'legs:{{id:"minecraft:netherite_leggings",count:1}},'
        f'feet:{{id:"minecraft:netherite_boots",count:1}}'
        f'}}'
        f'}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 04
# 本棚・エンチャント・醸造
# ============================================================

def step04():

    step_no = 4
    action = 0

    step_start(step_no, "本棚・エンチャント・醸造")

    action += 1
    step_action(step_no, action, "模様入り本棚")
    cmd(f"setblock {pos(-10,0,-5)} minecraft:chiseled_bookshelf")

    action += 1
    step_action(step_no, action, "エンチャントテーブル")
    cmd(f"setblock {pos(-9,0,-5)} minecraft:enchanting_table")

    action += 1
    step_action(step_no, action, "醸造台")
    cmd(f"setblock {pos(-8,0,-5)} minecraft:brewing_stand")

    step_complete(step_no)


# ============================================================
# STEP 05
# 溶鉱炉・ダブルチェスト
# ============================================================

def step05():

    step_no = 5
    action = 0

    step_start(step_no, "溶鉱炉・ダブルチェスト")

    action += 1
    step_action(step_no, action, "溶鉱炉")

    cmd(
        f"setblock {pos(-7,0,-5)} "
        f"minecraft:blast_furnace[facing=south]"
    )

    action += 1
    step_action(step_no, action, "チェスト左")

    cmd(
        f"setblock {pos(-6,0,-5)} "
        f"minecraft:chest[facing=south,type=right]"
    )

    action += 1
    step_action(step_no, action, "チェスト右")

    cmd(
        f"setblock {pos(-5,0,-5)} "
        f"minecraft:chest[facing=south,type=left]"
    )

    action += 1
    step_action(step_no, action, "チェスト内容")

    cmd(
        f'/data merge block {pos(-6,0,-5)} '
        f'{{Items:['
        f'{{Slot:0b,id:"minecraft:cobblestone",count:64}},'
        f'{{Slot:1b,id:"minecraft:iron_ingot",count:64}},'
        f'{{Slot:2b,id:"minecraft:stone_pickaxe",count:1}},'
        f'{{Slot:3b,id:"minecraft:shield",count:1}},'
        f'{{Slot:4b,id:"minecraft:bow",count:1}},'
        f'{{Slot:5b,id:"minecraft:arrow",count:64}},'
        f'{{Slot:6b,id:"minecraft:trident",count:1}},'
        f'{{Slot:7b,id:"minecraft:obsidian",count:64}},'
        f'{{Slot:8b,id:"minecraft:crying_obsidian",count:64}},'
        f'{{Slot:9b,id:"minecraft:diamond",count:64}},'
        f'{{Slot:10b,id:"minecraft:dried_ghast",count:1}},'
        f'{{Slot:11b,id:"minecraft:sniffer_egg",count:1}},'
        f'{{Slot:12b,id:"minecraft:wheat_seeds",count:64}},'
        f'{{Slot:13b,id:"minecraft:blaze_rod",count:64}},'
        f'{{Slot:14b,id:"minecraft:dragon_egg",count:1}},'
        f'{{Slot:15b,id:"minecraft:dragon_breath",count:64}},'
        f'{{Slot:16b,id:"minecraft:elytra",count:1}},'
        f'{{Slot:17b,id:"minecraft:pumpkin",count:64}}'
        f']}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 06
# ベッド・村人
# ============================================================

def step06():

    step_no = 6
    action = 0

    step_start(step_no, "ベッド・村人")

    action += 1
    step_action(step_no, action, "ベッド FOOT")

    cmd(
        f"setblock {pos(-4,0,-5)} "
        f"minecraft:red_bed[facing=south,part=foot]"
    )

    action += 1
    step_action(step_no, action, "ベッド HEAD")

    cmd(
        f"setblock {pos(-4,0,-4)} "
        f"minecraft:red_bed[facing=south,part=head]"
    )

    action += 1
    step_action(step_no, action, "村人")

    cmd(
        f'summon minecraft:villager {pos(-3,0,-5)} '
        f'{{'
        f'VillagerData:{{level:5,profession:"minecraft:farmer",type:"minecraft:plains"}},'
        f'Silent:1b,'
        f'Invulnerable:1b,'
        f'NoAI:1b,'
        f'Offers:{{Recipes:['
        f'{{buy:{{id:"minecraft:emerald",count:1}},'
        f'sell:{{id:"minecraft:snowball",count:1}},'
        f'maxUses:9999}}'
        f']}}'
        f'}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 07
# スケルトン・看板・作業台
# ============================================================

def step07():

    step_no = 7
    action = 0

    step_start(step_no, "スケルトン・看板・作業台")

    action += 1
    step_action(step_no, action, "スケルトン")

    cmd(
        f'summon minecraft:skeleton {pos(-2,0,-5)} '
        f'{{'
        f'NoAI:1b,'
        f'PersistenceRequired:1b,'
        f'Health:2f,'
        f'Rotation:[0f,0f]'
        f'}}'
    )

    action += 1
    step_action(step_no, action, "看板")

    cmd(
        f'setblock {pos(-1,0,-5)} '
        f'minecraft:oak_sign[rotation=0]'
        f'{{front_text:{{messages:['
        f'"","crocadooo","",""]}}}}'
    )

    action += 1
    step_action(step_no, action, "作業台")

    cmd(
        f"setblock {pos(0,0,-5)} "
        f"minecraft:crafting_table"
    )

    step_complete(step_no)


# ============================================================
# STEP 08
# 動物
# ============================================================

def step08():

    step_no = 8
    action = 0

    step_start(step_no, "動物")

    action += 1
    step_action(step_no, action, "オウム")

    cmd(
        f'summon minecraft:parrot {pos(1,0,-5)} '
        f'{{NoAI:1b,Silent:1b,Rotation:[0f,0f]}}'
    )

    action += 1
    step_action(step_no, action, "アルマジロ")

    cmd(
        f'summon minecraft:armadillo {pos(2,0,-5)} '
        f'{{NoAI:1b,Silent:1b,Rotation:[0f,0f]}}'
    )

    action += 1
    step_action(step_no, action, "アレイ")

    cmd(
        f'summon minecraft:allay {pos(3,0,-5)} '
        f'{{Silent:1b,NoGravity:1b,PersistenceRequired:1b}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 09
# 金ブロック＋コマンドブロック
# ============================================================

def step09():

    step_no = 9
    action = 0

    step_start(step_no, "金ブロック＋コマンドブロック")

    action += 1
    step_action(step_no, action, "金ブロック")

    cmd(
        f"setblock {pos(10,-1,-5)} "
        f"minecraft:gold_block"
    )

    action += 1
    step_action(step_no, action, "リピートコマンドブロック")

    command = (
        f'execute as @a at @s '
        f'if block ~ ~-1 ~ minecraft:gold_block '
        f'run setblock {pos(10,0,-7)} '
        f'minecraft:suspicious_sand'
    )

    cmd(
        f'setblock {pos(10,-2,-5)} '
        f'minecraft:repeating_command_block'
        f'{{auto:1b,Command:"{command}"}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 10
# TP装置
# ============================================================

def step10():

    step_no = 10
    action = 0

    step_start(step_no, "TP装置")

    action += 1
    step_action(step_no, action, "コマンドブロック")

    tp_command = (
        f"tp @p {pos(0,1,0)}"
    )

    cmd(
        f'setblock {pos(11,-1,-5)} '
        f'minecraft:command_block'
        f'{{Command:"{tp_command}"}}'
    )

    action += 1
    step_action(step_no, action, "見た目ブロック")

    cmd(
        f"setblock {pos(11,0,-5)} "
        f"minecraft:stone"
    )

    action += 1
    step_action(step_no, action, "ボタン")

    cmd(
        f"setblock {pos(11,0,-4)} "
        f"minecraft:stone_button[facing=south]"
    )

    step_complete(step_no)


# ============================================================
# STEP 11
# クリック看板
# ============================================================

def step11():

    step_no = 11
    action = 0

    step_start(step_no, "クリック看板")

    action += 1
    step_action(step_no, action, "看板設置")

    cmd(
        f"setblock {pos(12,0,-5)} "
        f"minecraft:oak_sign"
    )

    action += 1
    step_action(step_no, action, "看板データ")

    sign_command = (
        'data merge block '
        f'{pos(12,0,-5)} '
        '{"front_text":{"messages":['
        '"{\\"text\\":\\"ダイヤGET\\",'
        '\\"clickEvent\\":{'
        '\\"action\\":\\"run_command\\",'
        '\\"value\\":\\"give @s minecraft:diamond 1\\"'
        '}}"'
        ',"","",""]}}'
    )

    cmd(sign_command)

    step_complete(step_no)


# ============================================================
# STEP 12
# 水・溶岩
# ============================================================

def step12():

    step_no = 12
    action = 0

    step_start(step_no, "水・溶岩・水生生物")

    action += 1
    step_action(step_no, action, "水")

    cmd(
        f"fill "
        f"{pos(-5,-1,0)} "
        f"{pos(-2,-1,1)} "
        f"minecraft:water"
    )

    action += 1
    step_action(step_no, action, "溶岩")

    cmd(
        f"fill "
        f"{pos(2,-1,0)} "
        f"{pos(2,-1,1)} "
        f"minecraft:lava"
    )

    action += 1
    step_action(step_no, action, "ウーパールーパー")

    cmd(
        f'summon minecraft:axolotl {pos(-3,-1,0)} '
        f'{{NoAI:1b}}'
    )

    action += 1
    step_action(step_no, action, "オタマジャクシ")

    cmd(
        f'summon minecraft:tadpole {pos(-5,-1,1)} '
        f'{{NoAI:1b}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 13
# ネザーゲート
# ============================================================

def step13():

    step_no = 13
    action = 0

    step_start(step_no, "ネザーゲート")

    BASE_X = 5
    BASE_Y = -1
    BASE_Z = -5

    for dy in range(5):

        for dx in range(4):

            if dx in [0, 3] or dy in [0, 4]:
                block = "minecraft:obsidian"
            else:
                block = "minecraft:air"

            action += 1

            step_action(
                step_no,
                action,
                f"ゲートブロック ({dx},{dy})"
            )

            cmd(
                f"setblock "
                f"{pos(BASE_X+dx, BASE_Y+dy, BASE_Z)} "
                f"{block}"
            )

    action += 1
    step_action(step_no, action, "ゲート点火")

    cmd(
        f"setblock "
        f"{pos(BASE_X+1,BASE_Y+1,BASE_Z)} "
        f"minecraft:fire"
    )

    step_complete(step_no)


# ============================================================
# STEP 14
# アイテム配布
# ============================================================

def step14():

    step_no = 14
    action = 0

    step_start(step_no, "テストアイテム配布")

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
        "minecraft:compass 1"
    ]

    for item in items:

        action += 1

        step_action(
            step_no,
            action,
            f"give {item.split()[0]}"
        )

        cmd(f"give @a {item}")

    step_complete(step_no)


# ============================================================
# STEP 15
# オオカミ＋骨チェスト
# ============================================================

def step15():

    step_no = 15
    action = 0

    step_start(step_no, "オオカミ＋骨チェスト")

    WOLF_VARIANTS = [
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
        "grumpy"
    ]

    base_x = -11
    z_line = -10

    for i, variant in enumerate(WOLF_VARIANTS):

        action += 1

        step_action(
            step_no,
            action,
            f"オオカミ {variant}"
        )

        cmd(
            f'summon minecraft:wolf '
            f'{pos(base_x+i,0,z_line)} '
            f'{{'
            f'NoAI:1b,'
            f'Sitting:1b,'
            f'Silent:1b,'
            f'CollarColor:14b,'
            f'variant:"minecraft:{variant}",'
            f'sound_variant:"minecraft:{variant}"'
            f'}}'
        )

    action += 1
    step_action(step_no, action, "骨チェスト設置")

    cmd(
        f"setblock {pos(-12,0,-10)} "
        f"minecraft:chest[facing=south]"
    )

    action += 1
    step_action(step_no, action, "骨を投入")

    cmd(
        f'/data merge block {pos(-12,0,-10)} '
        f'{{Items:['
        f'{{Slot:0b,id:"minecraft:bone",count:64}},'
        f'{{Slot:1b,id:"minecraft:bone",count:64}},'
        f'{{Slot:2b,id:"minecraft:bone",count:64}},'
        f'{{Slot:3b,id:"minecraft:bone",count:64}},'
        f'{{Slot:4b,id:"minecraft:bone",count:64}},'
        f'{{Slot:5b,id:"minecraft:bone",count:64}},'
        f'{{Slot:6b,id:"minecraft:bone",count:64}},'
        f'{{Slot:7b,id:"minecraft:bone",count:64}}'
        f']}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 16
# 猫＋魚チェスト
# ============================================================

def step16():

    step_no = 16
    action = 0

    step_start(step_no, "猫＋魚チェスト")

    CAT_VARIANTS = [
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
        "all_black"
    ]

    base_x = -11
    z_line = -14

    for i, variant in enumerate(CAT_VARIANTS):

        action += 1

        step_action(
            step_no,
            action,
            f"猫 {variant}"
        )

        cmd(
            f'summon minecraft:cat '
            f'{pos(base_x+i,0,z_line)} '
            f'{{'
            f'NoAI:1b,'
            f'Sitting:1b,'
            f'Silent:1b,'
            f'variant:"minecraft:{variant}"'
            f'}}'
        )

    action += 1
    step_action(step_no, action, "魚チェスト設置")

    cmd(
        f"setblock {pos(-12,0,-14)} "
        f"minecraft:chest[facing=south]"
    )

    action += 1
    step_action(step_no, action, "魚を投入")

    cmd(
        f'/data merge block {pos(-12,0,-14)} '
        f'{{Items:['
        f'{{Slot:0b,id:"minecraft:cod",count:64}},'
        f'{{Slot:1b,id:"minecraft:cod",count:64}},'
        f'{{Slot:2b,id:"minecraft:salmon",count:64}},'
        f'{{Slot:3b,id:"minecraft:salmon",count:64}}'
        f']}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 17
# カエル＋リードチェスト
# ============================================================

def step17():

    step_no = 17
    action = 0

    step_start(step_no, "カエル＋リードチェスト")

    FROG_VARIANTS = [
        "temperate",
        "warm",
        "cold"
    ]

    base_x = -11
    z_line = -18

    for i, variant in enumerate(FROG_VARIANTS):

        action += 1

        step_action(
            step_no,
            action,
            f"カエル {variant}"
        )

        cmd(
            f'summon minecraft:frog '
            f'{pos(base_x+i,0,z_line)} '
            f'{{'
            f'NoAI:1b,'
            f'Silent:1b,'
            f'variant:"minecraft:{variant}"'
            f'}}'
        )

    action += 1
    step_action(step_no, action, "リードチェスト設置")

    cmd(
        f"setblock {pos(-12,0,-18)} "
        f"minecraft:chest[facing=south]"
    )

    action += 1
    step_action(step_no, action, "リードを投入")

    cmd(
        f'/data merge block {pos(-12,0,-18)} '
        f'{{Items:['
        f'{{Slot:0b,id:"minecraft:lead",count:64}},'
        f'{{Slot:1b,id:"minecraft:lead",count:64}},'
        f'{{Slot:2b,id:"minecraft:lead",count:64}}'
        f']}}'
    )

    step_complete(step_no)


# ============================================================
# STEP 99
# 完了
# ============================================================

def step99():

    separator()
    msg("========================================")
    msg("[ADVTEST] STAGE GENERATION COMPLETE")
    msg("========================================")
    msg("")
    msg("Minescriptによるステージ生成が完了しました。")
    msg("")
    msg("ここから先はSkript側でゲームをテストしてください。")
    msg("")
    msg("Minescript : ステージ生成")
    msg("Skript     : ゲームシステム")
    msg("")
    msg("========================================")


# ============================================================
# STEP一覧
# ============================================================

STEPS = [
    step01,
    step02,
    step03,
    step04,
    step05,
    step06,
    step07,
    step08,
    step09,
    step10,
    step11,
    step12,
    step13,
    step14,
    step15,
    step16,
    step17,
]


# ============================================================
# キー入力待機
# ============================================================

def wait_for_enter_or_escape(event_queue):

    while True:

        event = event_queue.get()

        # ----------------------------------------------------
        # キーイベント以外は無視
        # ----------------------------------------------------

        if event.type != m.EventType.KEY:
            continue

        # ----------------------------------------------------
        # ESC
        # ----------------------------------------------------

        if event.key == KEY_ESCAPE and event.action == 1:

            separator()
            msg("[ADVTEST] 中断しました。")
            msg("現在のステージ状態はそのまま残ります。")
            separator()

            return False

        # ----------------------------------------------------
        # ENTER
        # ----------------------------------------------------

        if event.key == KEY_ENTER and event.action == 1:

            return True


# ============================================================
# メイン
# ============================================================

def main():

    # --------------------------------------------------------
    # 開始表示
    # --------------------------------------------------------

    separator()
    msg("========================================")
    msg("[ADVTEST] TEST STAGE GENERATOR")
    msg("========================================")
    msg("")
    msg("Minecraft 26.2")
    msg("Minescript Stage Generator")
    msg("")
    msg("プレイヤー位置を基準にステージを生成します。")
    msg("")
    msg("Enter : 次のSTEP")
    msg("ESC   : 中断")
    msg("")
    msg("========================================")

    # --------------------------------------------------------
    # EventQueue
    # --------------------------------------------------------

    with m.EventQueue() as event_queue:

        # キーボードイベントを登録
        event_queue.register_key_listener()

        # ----------------------------------------------------
        # STEPを順番に実行
        # ----------------------------------------------------

        for index, step_function in enumerate(STEPS):

            step_number = index + 1

            try:

                # STEP実行
                step_function()

            except Exception as e:

                # Python側の例外
                step_error(
                    step_number,
                    0,
                    str(e)
                )

                msg("ステージ生成を停止しました。")
                msg("latest.logも確認してください。")

                return

            # ------------------------------------------------
            # 最後のSTEPなら終了
            # ------------------------------------------------

            if step_number == len(STEPS):

                break

            # ------------------------------------------------
            # Enter / ESC待機
            # ------------------------------------------------

            if not wait_for_enter_or_escape(event_queue):

                return

        # ----------------------------------------------------
        # 完了
        # ----------------------------------------------------

        step99()


# ============================================================
# 実行
# ============================================================

if __name__ == "__main__":
    main()