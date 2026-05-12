import minescript as m
import time
import sys

argv = sys.argv

# --- Argument handling ---
arg1 = argv[1] if len(argv) > 1 else (m.echo("Please specify a command: get / start") or sys.exit(1))

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
# start : Infinite rockets
# =========================
elif arg1 == "start":
    m.echo("☁ Aerial stroll started")

    while True:
        hands = m.player_hand_items()

        main = hands.main_hand

        # --- 形式に応じて取得 ---
        if isinstance(main, dict):
            main_item = main.get("item", "minecraft:air")
        elif main:
            main_item = getattr(main, "item", "minecraft:air")
        else:
            main_item = "minecraft:air"

        if main_item != "minecraft:firework_rocket":
            m.execute(
                "item replace entity @p weapon.mainhand with minecraft:firework_rocket 1"
            )
            m.execute("xp add @p 3 points")

        time.sleep(1)

# =========================
# Unknown command
# =========================
else:
    m.echo("Unknown command. Use: get / start")
