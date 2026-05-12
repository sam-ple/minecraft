import minescript as m
import time
import sys
import re

argv = sys.argv

# --- Argument handling ---
arg1 = argv[1] if len(argv) > 1 else (m.echo("Please specify a command: start") or sys.exit(1))

def extract_brace_block(text, start_key):
    start = text.find(start_key)
    if start == -1:
        return None

    # 最初の { の位置へ
    start = text.find("{", start)
    if start == -1:
        return None

    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                return text[start:i+1]

    return None


# =========================
# get : Give Elytra
# =========================
if arg1 == "get":
    m.execute('/title @a title {"text":"Elytra Ready","color":"aqua","bold":true}')

    # Replace main hand with Elytra
    m.execute("/item replace entity @p weapon.mainhand with minecraft:elytra")

    # Apply enchantments
    enchants = [
        "minecraft:mending 1",
        "minecraft:unbreaking 3"
    ]
    for ench in enchants:
        m.execute(f"/enchant @p {ench}")

    m.echo("🪽 Elytra equipped (Mending I / Unbreaking III)")

# =========================
# nbt
# =========================
elif arg1 == "nbt":

    p = m.player(nbt=True)

    if not p.nbt:
        print("NBT not available")
        exit()

    nbt = p.nbt

    print("========== RAW PLAYER NBT ==========")
    print(nbt)
    print("====================================")

    # -------------------------------------------------
    # Elytra存在確認
    # -------------------------------------------------
    if "minecraft:elytra" in nbt:
        print("Elytra detected in NBT.")
    else:
        print("No Elytra found in player NBT.")

    # # -------------------------------------------------
    # # SLOT 0（SelectedItemから取得）
    # # -------------------------------------------------
    # slot0_item = None

    # selected_match = re.search(
    #     r'SelectedItem:(\{.*?\}),SelectedItemSlot',
    #     nbt
    # )

    # if selected_match:
    #     slot0_item = selected_match.group(1)

    # # -------------------------------------------------
    # # チェスト装備抽出（1.21対応）
    # # equipment:{chest:{...}}
    # # -------------------------------------------------
    # chest_item = None

    # chest_match = re.search(
    #     r'equipment:\{chest:(\{.*?\})\},',
    #     nbt
    # )

    # if chest_match:
    #     chest_item = chest_match.group(1)

    # SLOT 0
    slot0_item = extract_brace_block(nbt, "SelectedItem:")

    # CHEST
    chest_item = extract_brace_block(nbt, "chest:")


    # -------------------------------------------------
    # 出力
    # -------------------------------------------------
    print("\n========== SLOT 0 ==========")
    if slot0_item:
        print(slot0_item)
    else:
        print("Empty")

    print("\n========== CHEST EQUIPMENT ==========")
    if chest_item:
        print(chest_item)
    else:
        print("Empty")

# =========================
# set
# =========================
elif arg1 == "set":
    m.execute('/item replace entity @p armor.chest with minecraft:elytra[unbreakable={show_in_tooltip:false}]')
    # m.execute(
    # '/item replace entity @p armor.chest with minecraft:elytra'
    # '[minecraft:enchantments={levels:{minecraft:mending:1,minecraft:unbreaking:3}}]'
    # )

# =========================
# start 
# =========================
elif arg1 == "start":
    m.echo("☁ Aerial stroll started")

    while True:

        # --- ロケット補充 ---
        hands = m.player_hand_items()
        main = hands.main_hand

        if isinstance(main, dict):
            main_item = main.get("item", "minecraft:air")
        elif main:
            main_item = getattr(main, "item", "minecraft:air")
        else:
            main_item = "minecraft:air"

        if main_item != "minecraft:firework_rocket":
            # ロケットを渡す
            m.execute('/item replace entity @p weapon.mainhand with minecraft:firework_rocket 1')
            # m.execute("xp add @p 3 points")
            # m.execute('/execute at @p run summon minecraft:experience_orb ~ ~0.3 ~ {Value:20}')

            time.sleep(0.1)

            # 右クリック開始
            m.player_press_use(True)

            time.sleep(0.2)

            # 右クリック離す
            m.player_press_use(False)

        time.sleep(10)

# =========================
# start2
# =========================
elif arg1 == "start2":

    # ====== CONFIG ======
    TARGET_Y = 170          # ★維持したい高度（Y座標）。山対策で高め推奨
    PITCH_CRUISE = -7       # ★巡航角度（緩やかな前進用）
    PITCH_UP = -20          # ★高度が低い時の上昇角度
    PITCH_DOWN = 5          # ★高度が高すぎる時の下降角度
    ROCKET_COOLDOWN = 5     # ★ロケット再使用までの最低ループ回数（消費抑制）
    LOOP_INTERVAL = 1.0     # ★制御ループ間隔（秒）※1秒でゆったり制御

    tick_counter = 0
    last_rocket_tick = -999

    m.echo("☁ Auto flight started")

    # ===== 前進開始 =====
    m.player_press_forward(True)

    # ===== 離陸（ジャンプ2回で滑空）=====
    m.player_press_jump(True)
    time.sleep(0.2)
    m.player_press_jump(False)
    time.sleep(0.2)

    m.player_press_jump(True)
    time.sleep(0.2)
    m.player_press_jump(False)
    time.sleep(0.5)

    # ===== 初速ロケット（必ず補充してから使用）=====
    m.execute('/item replace entity @p weapon.mainhand with minecraft:firework_rocket 1')
    time.sleep(0.1)

    m.player_press_use(True)
    time.sleep(0.2)
    m.player_press_use(False)

    last_rocket_tick = 0
    
    # ===== メイン巡航ループ =====
    while True:
        tick_counter += 1

        # --- ロケット自動補充 ---
        hands = m.player_hand_items()
        main = hands.main_hand
        main_item = getattr(main, "item", "minecraft:air") if main else "minecraft:air"

        if main_item != "minecraft:firework_rocket":
            m.execute('/item replace entity @p weapon.mainhand with minecraft:firework_rocket 1')
            time.sleep(0.1)

        # --- 現在座標取得 ---
        pos = m.player_position()
        yaw, pitch = m.player_orientation()
        y = pos[1]

        # ===== 高度制御ロジック =====
        if y < TARGET_Y - 3:
            # 目標より低い → 上昇
            m.player_set_orientation(yaw, PITCH_UP)

            # 大きく低下している場合のみロケット使用
            if y < TARGET_Y - 10:
                if tick_counter - last_rocket_tick > ROCKET_COOLDOWN:
                    m.player_press_use(True)
                    time.sleep(0.2)
                    m.player_press_use(False)
                    last_rocket_tick = tick_counter

        elif y > TARGET_Y + 5:
            # 高すぎる → やや下降
            m.player_set_orientation(yaw, PITCH_DOWN)

        else:
            # 安定巡航
            m.player_set_orientation(yaw, PITCH_CRUISE)

        time.sleep(LOOP_INTERVAL)

# =========================
# Unknown command
# =========================
else:
    m.echo("Unknown command. Use: start")
