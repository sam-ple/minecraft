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

def get_targeted_entity(max_distance=6):
    return m.player_get_targeted_entity(max_distance=max_distance)

def get_closest_entity_within(radius=6):
    entities = m.entities()
    px, py, pz = m.player_position()
    player_name = m.player_name()  # プレイヤー名取得
    closest = None
    min_dist = float("inf")

    for e in entities:
        if e.name == player_name:
            continue  # 自分自身は除外！

        ex, ey, ez = e.position
        dist = ((ex - px) ** 2 + (ey - py) ** 2 + (ez - pz) ** 2) ** 0.5
        if dist < radius and e.type.startswith("entity.minecraft."):
            if dist < min_dist:
                min_dist = dist
                closest = e
    return closest

def main():
    m.echo("🎯 Mob catcher started! Look at a mob and press [Enter] to catch it.")

    with EventQueue() as eq:
        eq.register_key_listener()

        while True:
            event = eq.get()

            if event.type == EventType.KEY and event.action == 1 and event.key in (257, 335):
                m.execute("say [DEBUG] Enter key pressed")

                target = get_targeted_entity()
                if target is None:
                    m.execute("say No direct target. Trying fallback.")
                    target = get_closest_entity_within()

                if target is None:
                    m.execute("say No mob found nearby.")
                    continue

                mob_type = target.type
                if not mob_type.startswith("entity.minecraft."):
                    m.execute("say Invalid target — not a mob.")
                    continue

                m.execute(f"say Targeted mob: {mob_type}")
                give_spawn_egg(mob_type)

                try:
                    m.execute(f"kill {target.uuid}")
                except:
                    try:
                        m.execute(f"kill {target.selector}")
                    except:
                        m.execute("say Failed to kill mob.")

                time.sleep(0.5)

if __name__ == "__main__":
    main()
