import minescript as m
import time

/particle minecraft:blue_flame_particle ~ ~1 ~
/particle <name> <pos> <delta> <speed> <count> [mode] [viewers]
/particle minecraft:flame ~ ~1 ~ 0 0 0 0.1 20 force

particles = [
    "angry_villager", "ash", "bubble", "cloud", "crit", "damage_indicator", "dragon_breath",
    "enchant", "end_rod", "explosion", "explosion_emitter", "flame", "happy_villager", "heart",
    "instant_effect", "large_smoke", "lava", "note", "poof", "portal", "rain", "smoke", "sneeze",
    "snowflake", "soul", "soul_fire_flame", "spit", "splash", "squid_ink", "sweep_attack",
    "totem_of_undying", "underwater", "white_ash", "white_smoke", "witch"
]

for p in particles:
    m.echo(f"Showing: {p}")
#    m.execute(f"particle minecraft:{p} ~ ~1 ~")
    m.execute(f"particle minecraft:{p} ~ ~2 ~ 0 0 0 0.1 20 force")
    time.sleep(2)
