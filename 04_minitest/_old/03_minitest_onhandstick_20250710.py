import minescript as m
import time

player = m.player_name()
already_held = False

m.echo("Will react when you hold a stick in your main hand.")

while True:
    hands = m.player_hand_items()
    main_hand = getattr(hands, "main_hand", None)

    if main_hand and getattr(main_hand, "item", "") == "minecraft:stick":
        if not already_held:
            m.chat(f"{player} has held a stick!")
            already_held = True
    else:
        already_held = False

    time.sleep(0.1)
