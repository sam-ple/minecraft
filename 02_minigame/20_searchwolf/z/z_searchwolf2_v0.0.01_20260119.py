import minescript as m
from minescript import EventQueue, EventType, execute, echo
from time import sleep, time
import json, os, re

# ==================================================
# Configuration
# ==================================================
SAVE_FILE = "wolf_variants.json"
ALL_WOLF_VARIANTS = {
    "pale", "woods", "ashen", "black", "chestnut",
    "rusty", "spotted", "striped", "snowy",
    "classic", "big", "grumpy"
}
DATA_PATTERN = re.compile(r'Wolf has the following entity data: "minecraft:(\w+)"')
CHECK_INTERVAL = 0.1  # イベント待機用

# ==================================================
# Load / Save
# ==================================================
def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()

def save_progress():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen_variants), f, indent=2, ensure_ascii=False)

seen_variants = load_progress()

# ==================================================
# Helpers
# ==================================================
def firework():
    execute(
        'execute at @p run summon firework_rocket ~ ~1 ~ '
        '{LifeTime:30,FireworksItem:{id:"minecraft:firework_rocket",Count:1,'
        'tag:{Fireworks:{Flight:1,Explosions:[{Type:1,Colors:[I;16711680,65280,255],'
        'FadeColors:[I;16777215]}]}}}}'
    )

def show_status():
    remaining = ALL_WOLF_VARIANTS - seen_variants
    echo(f"🐺 {len(seen_variants)}/{len(ALL_WOLF_VARIANTS)} collected")
    if remaining:
        echo("Remaining: " + ", ".join(sorted(remaining)))

# ==================================================
# Event Queue
# ==================================================
eq = EventQueue()
eq.register_chat_listener()
eq.register_damage_listener()

# クエリ済みの狼UUIDを保持して二重取得防止
queried_wolves = set()

echo("🐺 Wolf Variant Adventure (Attack to discover!)")
show_status()

# ==================================================
# Main Loop
# ==================================================
while True:
    try:
        event = eq.get(timeout=CHECK_INTERVAL)
    except Exception:
        sleep(CHECK_INTERVAL)
        continue

    # ----------------------------------
    # ダメージイベントで叩いた場合
    # ----------------------------------
    if event.type == EventType.DAMAGE:
        victim_list = m.entities(uuid=event.entity_uuid)
        attacker_list = m.players(uuid=event.cause_uuid)
        if not victim_list:
            continue
        victim = victim_list[0]
        if victim.type != "entity.minecraft.wolf":
            continue

        wolf_uuid = victim.uuid
        attacker_name = attacker_list[0].name if attacker_list else "Someone"

        # すでにクエリ済みならスキップ
        if wolf_uuid in queried_wolves:
            continue
        queried_wolves.add(wolf_uuid)

        # バリエーション取得
        execute(f"data get entity {wolf_uuid} variant")
        echo(f"💥 {attacker_name} hit a wolf! Querying variant...")

    # ----------------------------------
    # チャットで返ってきたvariantを取得
    # ----------------------------------
    elif event.type == EventType.CHAT:
        match = DATA_PATTERN.search(event.message)
        if match:
            variant = match.group(1)
            if variant not in ALL_WOLF_VARIANTS:
                echo(f"❓ Unknown variant: {variant}")
            elif variant not in seen_variants:
                seen_variants.add(variant)
                save_progress()
                echo(f"🆕 New Wolf Variant: {variant}")
                firework()
                show_status()

    sleep(CHECK_INTERVAL)
