# ============================================================
# 10 MINUTES CHALLENGE SYSTEM
# Version : v0.1.00
# Date: 2026-03-09
#
# Minecraft Java + MineScript
#
# Modes
#   iron   : フル鉄装備達成
#   adv    : 15アドバンスメント取得
#   nether : ネザー到達
#   inv    : インベントリ全種類
#
# Author : crocado
# ============================================================


# ============================================================
# Imports
# ============================================================

import minescript as m
from minescript import EventQueue, EventType

import sys
import time
import json
import re

from queue import Empty


# ============================================================
# CONFIG
# ============================================================

# 制限時間（秒）
DURATION = 600  # 10 minutes


# モード表示名
MODE_LABEL = {
    "iron": "FULL IRON",
    "adv": "15 ADV",
    "nether": "NETHER",
    "inv": "INVENTORY",
}


# ============================================================
# UTIL
# ============================================================

def sec_to_mmss(sec):
    """秒 → MM:SS 表示"""
    m_, s_ = divmod(int(sec), 60)
    return f"{m_:02d}:{s_:02d}"


def chat(msg, color="white"):
    """チャット表示"""
    m.execute(
        f'tellraw @a {json.dumps({"text": msg, "color": color})}'
    )


def title_main(msg, color="gold"):
    """タイトル表示"""
    m.execute(
        f'title @a title '
        f'{json.dumps({"text": msg, "color": color, "bold": True})}'
    )


def title_sub(msg, color="yellow"):
    """サブタイトル表示"""
    m.execute(
        f'title @a subtitle '
        f'{json.dumps({"text": msg, "color": color})}'
    )


# ============================================================
# CLEAR EFFECT
# ============================================================

def clear_effect(elapsed):
    """
    クリア演出
    ・タイトル
    ・サウンド
    ・花火
    """

    title_main("CLEAR!")
    title_sub(f"Time {elapsed}")

    # サウンド
    m.execute("playsound minecraft:ui.toast.challenge_complete master @a")
    m.execute("playsound minecraft:entity.firework_rocket.launch master @a")

    # 花火
    m.execute(
        "execute as @a at @s run summon firework_rocket ~ ~1 ~ "
        "{LifeTime:30}"
    )


# ============================================================
# COUNTDOWN
# ============================================================

def countdown(sec=3):
    """ゲーム開始カウントダウン"""

    for i in range(sec, 0, -1):
        title_main(str(i), "aqua")
        m.execute("playsound minecraft:block.note_block.pling master @a")
        time.sleep(1)

    title_main("START!")
    m.execute("playsound minecraft:entity.player.levelup master @a")
    time.sleep(1)


# ============================================================
# BOSSBAR
# ============================================================

last_boss_update = 0


def update_bossbar(remain):
    """
    BossBar更新
    ※1秒に1回だけ更新（負荷軽減）
    """

    global last_boss_update

    if time.time() - last_boss_update >= 1:

        m.execute(f"bossbar set tenmin value {remain}")

        m.execute(
            f'bossbar set tenmin name '
            f'{json.dumps({"text": sec_to_mmss(remain), "color": "gold"})}'
        )

        last_boss_update = time.time()


# ============================================================
# GAME STATE
# ============================================================

game_active = False
game_start_time = 0

# ADVモード用カウンタ
adv_count = 0


# ============================================================
# GAME START
# ============================================================

def start_game(mode):

    global game_active
    global game_start_time
    global adv_count

    # 基本設定
    m.execute("gamerule sendCommandFeedback false")
    m.execute("clear @a")
    m.execute("gamemode survival @a")

    # --------------------------
    # BossBar
    # --------------------------

    m.execute("bossbar remove tenmin")
    m.execute('bossbar add tenmin "Time"')

    m.execute("bossbar set tenmin players @a")
    m.execute(f"bossbar set tenmin max {DURATION}")
    m.execute(f"bossbar set tenmin value {DURATION}")

    # --------------------------
    # ADVモード用スコアボード
    # --------------------------

    if mode == "adv":

        m.execute("scoreboard objectives remove progress")

        m.execute(
            'scoreboard objectives add progress dummy "Advancements"'
        )

        m.execute(
            "scoreboard objectives setdisplay sidebar progress"
        )

        m.execute("scoreboard players set @a progress 0")

    adv_count = 0

    # カウントダウン
    countdown()

    game_active = True
    game_start_time = time.time()

    chat("⌛ 10 Minutes Challenge START", "aqua")
    chat(f"🎮 Mode: {MODE_LABEL[mode]}", "yellow")


# ============================================================
# GAME END
# ============================================================

def end_game(msg=None):

    global game_active

    if not game_active:
        return

    elapsed = sec_to_mmss(time.time() - game_start_time)

    if msg:

        chat(msg, "gold")
        chat(f"⏱ Clear Time: {elapsed}", "white")

        clear_effect(elapsed)

    else:

        chat("⏰ Time Up!", "red")

    game_active = False

    # 後処理
    m.execute("bossbar remove tenmin")
    m.execute("scoreboard objectives remove progress")

    m.execute("gamemode adventure @a")
    m.execute("gamerule sendCommandFeedback true")


# ============================================================
# MODE CHECKS
# ============================================================

# フル鉄装備スロット
IRON_ARMOR = {
    36: "minecraft:iron_boots",
    37: "minecraft:iron_leggings",
    38: "minecraft:iron_chestplate",
    39: "minecraft:iron_helmet",
}


def iron_clear():
    """
    フル鉄装備判定
    """

    inv = m.player_inventory()

    slots = {i.slot: i.item for i in inv if i}

    return all(
        slots.get(slot) == item
        for slot, item in IRON_ARMOR.items()
    )


def inv_clear():
    """
    インベントリ36種類判定
    同じアイテムがあれば失敗
    """

    inv = m.player_inventory()

    ids = set()

    for i in inv:

        if i and 0 <= i.slot <= 35:

            if i.item in ids:
                return False

            ids.add(i.item)

    return len(ids) == 36


# ============================================================
# ADVANCEMENT PARSER
# ============================================================

# チャットログからADV取得を検出
adv_pattern = re.compile(
    r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]"
)


# ============================================================
# ENTRY (ARGUMENT)
# ============================================================

if len(sys.argv) < 2:

    chat("Usage: /ms run 10min <iron|adv|nether|inv>", "red")
    sys.exit(0)


CURRENT_MODE = sys.argv[1]

if CURRENT_MODE not in MODE_LABEL:

    chat(f"Invalid mode: {CURRENT_MODE}", "red")
    sys.exit(0)


start_game(CURRENT_MODE)


# ============================================================
# EVENT LOOP
# ============================================================

eq = EventQueue()

# チャットイベント監視
eq.register_chat_listener()


while True:

    try:
        event = eq.get(timeout=0.1)

    except Empty:
        event = None


    # --------------------------
    # ゲーム進行
    # --------------------------

    if game_active:

        remain = max(
            DURATION - int(time.time() - game_start_time),
            0
        )

        update_bossbar(remain)

        # タイムアップ
        if remain <= 0:
            end_game()

        # モード判定
        if CURRENT_MODE == "iron" and iron_clear():
            end_game("⛓ FULL IRON CLEAR!")

        elif CURRENT_MODE == "inv" and inv_clear():
            end_game("🎒 INVENTORY COMPLETE!")


    # --------------------------
    # ADV / NETHER 判定
    # --------------------------

    if event and event.type == EventType.CHAT and game_active:

        msg = event.message.strip()

        m_ = adv_pattern.match(msg)

        if not m_:
            continue

        _, _, adv = m_.groups()

        # ----------------------
        # ADV MODE
        # ----------------------

        if CURRENT_MODE == "adv":

            adv_count += 1

            m.execute(
                f"scoreboard players set @a progress {adv_count}"
            )

            chat(f"📘 Advancement {adv_count}/15", "aqua")

            if adv_count >= 15:
                end_game("🏆 15 ADVANCEMENTS CLEAR!")


        # ----------------------
        # NETHER MODE
        # ----------------------

        elif CURRENT_MODE == "nether" and adv == "We Need to Go Deeper":

            end_game("🔥 ENTERED THE NETHER!")