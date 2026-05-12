import minescript as m
from minescript import EventQueue, EventType
import sys, time, json, re
from queue import Empty

# ==============================
# config
# ==============================
DURATION = 600  # 10 minutes

MODE_LABEL = {
    "iron": "FULL IRON",
    "adv": "15 ADV",
    "nether": "NETHER",
    "inv": "INVENTORY",
}

# ==============================
# utils
# ==============================
def sec_to_mmss(sec):
    m_, s_ = divmod(int(sec), 60)
    return f"{m_:02d}:{s_:02d}"

def chat(msg, color="white"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def title(msg, color="gold"):
    m.execute(
        f'title @a title {json.dumps({"text": msg, "color": color, "bold": True})}'
    )

# ==============================
# countdown
# ==============================
def countdown(sec=3):
    for i in range(sec, 0, -1):
        title(str(i), "aqua")
        m.execute("playsound minecraft:block.note_block.pling master @a")
        time.sleep(1)
    title("START!", "gold")
    m.execute("playsound minecraft:entity.player.levelup master @a")
    time.sleep(1)

# ==============================
# bossbar
# ==============================
last_boss_update = 0

def update_bossbar(remain):
    global last_boss_update
    if time.time() - last_boss_update >= 1:
        m.execute(f"bossbar set tenmin value {remain}")
        m.execute(
            f'bossbar set tenmin name {json.dumps({"text": sec_to_mmss(remain), "color": "gold"})}'
        )
        last_boss_update = time.time()

# ==============================
# game state
# ==============================
game_active = False
game_start_time = 0
adv_count = 0

# ==============================
# start / end
# ==============================
def start_game(mode):
    global game_active, game_start_time, adv_count

    m.execute("gamerule sendCommandFeedback false")
    m.execute("clear @a")
    m.execute("gamemode survival @a")

    m.execute("bossbar remove tenmin")
    m.execute('bossbar add tenmin "Time"')
    m.execute("bossbar set tenmin players @a")
    m.execute(f"bossbar set tenmin max {DURATION}")
    m.execute(f"bossbar set tenmin value {DURATION}")

    adv_count = 0

    countdown()

    game_active = True
    game_start_time = time.time()

    chat("⌛ 10 Minutes Challenge START", "aqua")
    chat(f"🎮 Mode: {MODE_LABEL[mode]}", "yellow")

def end_game(msg=None):
    global game_active

    if not game_active:
        return

    elapsed = sec_to_mmss(time.time() - game_start_time)

    if msg:
        chat(msg, "gold")
        chat(f"⏱ Clear Time: {elapsed}", "white")
    else:
        chat("⏰ Time Up!", "red")

    game_active = False
    m.execute("bossbar remove tenmin")
    m.execute("gamemode adventure @a")
    m.execute("gamerule sendCommandFeedback true")

# ==============================
# mode checks
# ==============================
IRON_ARMOR = {
    36: "minecraft:iron_boots",
    37: "minecraft:iron_leggings",
    38: "minecraft:iron_chestplate",
    39: "minecraft:iron_helmet",
}

def iron_clear():
    inv = m.player_inventory()
    slots = {i.slot: i.item for i in inv if i}
    return all(slots.get(s) == item for s, item in IRON_ARMOR.items())

def inv_clear():
    inv = m.player_inventory()
    ids = set()
    for i in inv:
        if i and 0 <= i.slot <= 35:
            if i.item.id in ids:
                return False
            ids.add(i.item)
    return len(ids) == 36

# ==============================
# advancement
# ==============================
adv_pattern = re.compile(
    r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]"
)

# ==============================
# entry (arg)
# ==============================
if len(sys.argv) < 2:
    chat("Usage: /ms run 10min <iron|adv|nether|inv>", "red")
    sys.exit(0)

CURRENT_MODE = sys.argv[1]

if CURRENT_MODE not in MODE_LABEL:
    chat(f"Invalid mode: {CURRENT_MODE}", "red")
    sys.exit(0)

start_game(CURRENT_MODE)

# ==============================
# event loop
# ==============================
eq = EventQueue()
eq.register_chat_listener()

while True:
    try:
        event = eq.get(timeout=0.1)
    except Empty:
        event = None

    if game_active:
        remain = max(DURATION - int(time.time() - game_start_time), 0)
        update_bossbar(remain)

        if remain <= 0:
            end_game()

        # -------- clear checks --------
        if CURRENT_MODE == "iron" and iron_clear():
            end_game("⛓ FULL IRON CLEAR!")
        elif CURRENT_MODE == "inv" and inv_clear():
            end_game("🎒 INVENTORY COMPLETE!")

    if event and event.type == EventType.CHAT and game_active:
        msg = event.message.strip()
        m_ = adv_pattern.match(msg)

        if m_:
            _, _, adv = m_.groups()

            if CURRENT_MODE == "adv":
                adv_count += 1
                if adv_count >= 15:
                    end_game("🏆 15 ADVANCEMENTS CLEAR!")

            if CURRENT_MODE == "nether" and adv == "We Need to Go Deeper":
                end_game("🔥 ENTERED THE NETHER!")
