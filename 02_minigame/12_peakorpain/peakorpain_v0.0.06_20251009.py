import minescript as m
import random, time

# ==============================
# 🔧 Settings
# ==============================
ROULETTE_INTERVAL = 180   # Roulette interval (seconds) → 3 min
DEFAULT_EFFECT_DURATION = 60  # Default effect duration (seconds)

players = ["crocadooo", "sampleeeeeee", "saaample", "Everyone"]
effects = [
    "👿 TNT at feet",
    "👼 Random ores at feet",
    "👿 Summon zombies when walking",
    "👼 Creative Mode",
    "👿 Half Heart",
    "👼 Invincible",
    "👼 Full Netherite Armor"
]

# ==============================
# 💣 Effect functions (placeholders)
# ==============================
def effect_tnt(target, duration=DEFAULT_EFFECT_DURATION):
    m.echo(f"TNT effect applied to {target} ({duration}s)")

def effect_random_ores(target, duration=DEFAULT_EFFECT_DURATION):
    m.echo(f"Random ores effect applied to {target} ({duration}s)")

def effect_zombie_spawn(target, duration=DEFAULT_EFFECT_DURATION):
    m.echo(f"Zombie spawn on walk effect applied to {target} ({duration}s)")

def effect_creative(target, duration=DEFAULT_EFFECT_DURATION):
    m.echo(f"Creative Mode effect applied to {target} ({duration}s)")

def effect_half_heart(target, duration=DEFAULT_EFFECT_DURATION):
    m.echo(f"Half Heart effect applied to {target} ({duration}s)")

def effect_invincible(target, duration=DEFAULT_EFFECT_DURATION):
    m.echo(f"Invincible effect applied to {target} ({duration}s)")

def effect_full_netherite(target, duration=DEFAULT_EFFECT_DURATION):
    m.echo(f"Full Netherite Armor effect applied to {target} ({duration}s)")

# ==============================
# ♻️ Reset
# ==============================
def reset(target="@a"):
    m.echo(f"🔄 Resetting status of {target}")
    # m.execute(f"gamemode survival {target}")
    # m.execute(f"attribute {target} minecraft:max_health base set 20")
    # m.execute(f"effect clear {target}")
    # m.execute(f"effect give {target} minecraft:instant_health 1 1 true")

# ==============================
# 🎰 Roulette
# ==============================
def spin_roulette():
    m.execute("bossbar remove roulette")
    m.execute('bossbar add roulette "🎲 Spinning the Roulette..."')
    m.execute('bossbar set roulette players @a')

    spins = random.randint(10, 15)
    result_player, result_effect = None, None

    for i in range(spins):
        p = random.choice(players)
        e = random.choice(effects)
        result_player, result_effect = p, e

        m.execute('playsound minecraft:block.note_block.hat master @a ~ ~ ~ 1 1.5')
        m.execute(f'title @a title ""')
        m.execute(f'title @a subtitle "▶ {p} × {e}"')
        m.execute(f'title @a actionbar "▶ {p} × {e}"')
        m.execute(f'bossbar set roulette name "🎲 {p} × {e}"')

        time.sleep(0.25 if i < spins - 3 else 0.5)

    # Announce result
    m.execute(f'title @a subtitle "★ {result_player} × {result_effect} ★"')
    m.execute(f'bossbar set roulette name "★ {result_player} × {result_effect} ★"')
    m.execute(f'tellraw @a {{"text":"🎲 Result: {result_player} × {result_effect}","color":"aqua"}}')

    target = "@a" if result_player == "Everyone" else result_player

    # Apply effect (placeholders)
    if "TNT" in result_effect:
        effect_tnt(target, 10)
    elif "Random ores" in result_effect:
        effect_random_ores(target, 10)
    elif "Zombie" in result_effect:
        effect_zombie_spawn(target, 10)
    elif "Creative" in result_effect:
        effect_creative(target, 30)
    elif "Half Heart" in result_effect:
        effect_half_heart(target, 45)
    elif "Invincible" in result_effect:
        effect_invincible(target, 60)
    elif "Netherite" in result_effect:
        effect_full_netherite(target, 60)
    else:
        reset(target)

# ==============================
# 🕹 Main loop
# ==============================
m.echo("🎰 Automatic roulette started!")
reset()

while True:
    spin_roulette()
    m.echo(f"⏳ Waiting {ROULETTE_INTERVAL} seconds until next roulette...")
    time.sleep(ROULETTE_INTERVAL)
