# Beginners Guide 04: Titles, Effects, Sounds, and Particles in Minescript
# Tutorial flow with intro/outro titles for each section

import minescript as m
import time

PLAYER = m.player_name()
BOSSBAR_ID = "minecraft:command_bar"

# --- Bossbar initialization ---
m.execute("gamerule sendCommandFeedback false")
m.execute(f"bossbar remove {BOSSBAR_ID}")  # remove old one if exists
m.execute(f"bossbar add {BOSSBAR_ID} Tutorial")
m.execute(f"bossbar set {BOSSBAR_ID} max 1")
m.execute(f"bossbar set {BOSSBAR_ID} players {PLAYER}")

def show_command(cmd: str):
    """Display executed command in bossbar and actionbar"""
    m.execute(f'bossbar set {BOSSBAR_ID} name {{"text":"{cmd}","color":"aqua"}}')
    m.execute(f'title {PLAYER} actionbar {{"text":"{cmd}","color":"gold"}}')

# ❶ Titles & Subtitles
def title_subtitle(title_text, subtitle_text=None, title_color="gold", subtitle_color="aqua", delay=2):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title_text}","color":"{title_color}","bold":true}}')
    if subtitle_text and subtitle_text.strip():
        m.execute(f'title @a subtitle {{"text":"{subtitle_text}","color":"{subtitle_color}","bold":true}}')
    show_command(f"/title @a title {title_text}")
    time.sleep(delay)

# ❷ Effects
def give_effect(target="@s", effect="speed", duration=8, level=1, hide_particles=False):
    hide = "true" if hide_particles else "false"
    cmd = f"/effect give {target} {effect} {duration} {level} {hide}"
    m.execute(cmd)
    show_command(cmd)

def clear_effects(target="@s"):
    cmd = f"/effect clear {target}"
    m.execute(cmd)
    show_command(cmd)

# ❸ Sounds
def play_sound(sound="minecraft:entity.player.levelup", source="master", target="@s", volume=1, pitch=1):
    cmd = f"/playsound {sound} {source} {target} ~ ~ ~ {volume} {pitch}"
    m.execute(cmd)
    show_command(cmd)

# ❹ Particles
def spawn_particle(particle="minecraft:happy_villager", x="~", y="~", z="~", dx=0, dy=0, dz=0, speed=0, count=1):
    cmd = f"/particle {particle} {x} {y} {z} {dx} {dy} {dz} {speed} {count}"
    m.execute(cmd)
    show_command(cmd)

# --- Demo sequence ---

# Section: Titles
title_subtitle("Section 1", "Titles & Subtitles", "yellow", "white", delay=3)
title_subtitle("Welcome!", "Have fun!", "gold", "aqua")
time.sleep(2)
title_subtitle("Level Up!", "You reached level 5", "green", "yellow")
time.sleep(2)
title_subtitle("Warning!", "Danger ahead!", "red", "dark_red")
time.sleep(2)
title_subtitle("Quest Complete!", "Reward obtained", "gold", "white")
time.sleep(2)
title_subtitle("Game Over", "Try again?", "dark_purple", "gray")
time.sleep(2)
title_subtitle("Titles Section", "Complete!", "dark_green", "white", delay=3)

# Section: Effects
title_subtitle("Section 2", "Effects Showcase", "yellow", "white", delay=3)
effects = [
    ("speed", 6, 2, False),
    ("jump_boost", 6, 3, False),
    ("strength", 6, 2, True),
    ("regeneration", 6, 2, False),
    ("resistance", 6, 1, True),
    ("invisibility", 6, 1, False),
    ("night_vision", 6, 1, True),
    ("fire_resistance", 6, 1, False),
    ("water_breathing", 6, 1, False),
    ("health_boost", 6, 3, True),
]
for effect, dur, lvl, hide in effects:
    give_effect(effect=effect, duration=dur, level=lvl, hide_particles=hide)
    time.sleep(dur + 1)

clear_effects()
title_subtitle("Effects Section", "Complete!", "dark_green", "white", delay=3)

# Section: Sounds
title_subtitle("Section 3", "Sounds Showcase", "yellow", "white", delay=3)
sounds = [
    "minecraft:entity.player.levelup",
    "minecraft:block.note_block.bell",
    "minecraft:entity.experience_orb.pickup",
    "minecraft:entity.firework_rocket.launch",
    "minecraft:entity.arrow.hit_player",
    "minecraft:entity.cat.ambient",
    "minecraft:entity.villager.celebrate",
    "minecraft:entity.zombie.attack_iron_door",
    "minecraft:block.anvil.land",
    "minecraft:music_disc.chirp",
]
for s in sounds:
    play_sound(s)
    time.sleep(3)
title_subtitle("Sounds Section", "Complete!", "dark_green", "white", delay=3)

# Section: Particles
title_subtitle("Section 4", "Particles Showcase", "yellow", "white", delay=3)
particles = [
    "minecraft:heart",
    "minecraft:happy_villager",
    "minecraft:flame",
    "minecraft:crit",
    "minecraft:dragon_breath",
    "minecraft:explosion",
    "minecraft:soul",
    "minecraft:totem_of_undying",
    "minecraft:enchant",
    "minecraft:note",
]
for p in particles:
    spawn_particle(p, dx=0.5, dy=1, dz=0.5, speed=0.1, count=10)
    time.sleep(3)
title_subtitle("Particles Section", "Complete!", "dark_green", "white", delay=3)

# Wrap up
title_subtitle("Demo Complete!", "Guide 04 finished", "dark_purple", "gray", delay=4)
