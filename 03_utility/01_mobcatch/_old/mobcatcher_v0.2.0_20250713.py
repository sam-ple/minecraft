import minescript as m
import time
from minescript import EventQueue, EventType

SPAWN_EGG_MAP = {
    "entity.minecraft.cow": "minecraft:cow_spawn_egg",
    "entity.minecraft.pig": "minecraft:pig_spawn_egg",
    "entity.minecraft.sheep": "minecraft:sheep_spawn_egg",
    "entity.minecraft.zombie": "minecraft:zombie_spawn_egg",
    "entity.minecraft.chicken": "minecraft:chicken_spawn_egg",
    "entity.minecraft.spider": "minecraft:spider_spawn_egg",
}

def give_spawn_egg(mob_type):
    egg = SPAWN_EGG_MAP.get(mob_type)
    if egg:
        m.execute(f"give {m.player_name()} {egg} 1")
        m.execute(f"say Spawn egg given: {egg}")
    else:
        m.execute(f"say No spawn egg mapping for mob type: {mob_type}")

def catch_mob(entity):
    mob_type = entity.type
    if not mob_type.startswith("entity.minecraft."):
        m.execute("say Invalid target — not a mob.")
        return

    m.execute(f"say Targeted mob: {mob_type}")
    give_spawn_egg(mob_type)

    try:
        m.execute(f"data merge entity {entity.uuid} {{NoAI:1b}}")
        m.execute(f"tp {entity.uuid} ~ 256 ~")
    except:
        try:
            m.execute(f"data merge entity {entity.selector} {{NoAI:1b}}")
            m.execute(f"tp {entity.selector} ~ 256 ~")
        except:
            m.execute("say Failed to teleport and freeze mob.")

def main():
    m.echo("Hold a stick and right-click a mob to catch it.")

    with EventQueue() as eq:
        eq.register_mouse_listener()

        while True:
            event = eq.get()

            # Right-click pressed (action == 1)
            if event.type == EventType.MOUSE and event.button == 1 and event.action == 1:
                hands = m.player_hand_items()
                main_hand = getattr(hands, "main_hand", None)
                if not (main_hand and getattr(main_hand, "item", "") == "minecraft:stick"):
                    continue

                target = m.player_get_targeted_entity(max_distance=6)
                if target is None:
                    m.execute("say No mob targeted.")
                    continue

                catch_mob(target)

                time.sleep(0.3)

if __name__ == "__main__":
    main()
