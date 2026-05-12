import minescript as m
from minescript import EventQueue, EventType

m.execute(f"give {m.player_name()} minecraft:clock 1")

x, y, z = m.player_position()
x, y, z = int(x), int(y), int(z)
m.echo(f"Current Position: X={x}, Y={y}, Z={z}")

m.execute(f"setblock {x} {y-1} {z} gold_block")

def main():
    m.echo("Hold a clock and release Left Shift to teleport!")

    with EventQueue() as eq:
        eq.register_key_listener()

        while True:
            event = eq.get()

            # Left Shift (key code 340) released
            if event.type == EventType.KEY and event.key == 340 and event.action == 0:
                hands = m.player_hand_items()
                main_hand = getattr(hands, "main_hand", None)

                if main_hand and getattr(main_hand, "item", "") == "minecraft:clock":
                    m.execute(f"tp {m.player_name()} {x} {y} {z}")
                    m.echo("Teleported when releasing Shift!")

if __name__ == "__main__":
    main()
