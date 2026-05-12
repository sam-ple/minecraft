import minescript as m
from minescript import EventQueue, EventType

def main():
    m.echo("Hold a clock and press Left Shift to teleport!")

    with EventQueue() as eq:
        eq.register_key_listener()

        while True:
            event = eq.get()

            # Left Shift (key code 340) pressed
            if event.type == EventType.KEY and event.key == 340 and event.action == 1:
                hands = m.player_hand_items()
                main_hand = getattr(hands, "main_hand", None)

                if main_hand and getattr(main_hand, "item", "") == "minecraft:clock":
                    m.execute(f"tp {m.player_name()} ~ ~10 ~")
                    m.echo("Teleported using Clock + Shift!")

if __name__ == "__main__":
    main()
