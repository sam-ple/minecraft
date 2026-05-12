import minescript as m
import random, time

m.execute("gamemode survival @a")
m.execute("attribute @a minecraft:max_health base set 20")
m.execute("effect give @a minecraft:instant_health 1 1 true")

players = ["crocadooo", "sampleeeeeee", "saaample", "Everyone"]
effects = ["Half Heart", "Full Health", "Creative Mode", "None"]

def apply_effect(player, effect):
    target = "@a" if player == "Everyone" else player
    
    # if effect == "TNT at feet":
    #     m.execute(f"execute as {target} at @s run summon tnt ~ ~ ~")
    if effect == "Half Heart":
        m.execute(f"attribute {target} minecraft:max_health base set 1")
    elif effect == "Full Health":
        m.execute(f"attribute {target} minecraft:max_health base set 40")
    elif effect == "Creative Mode":
        m.execute(f"gamemode creative {target}")
    elif effect == "None":
        pass

# Initialize bossbar
m.execute("bossbar remove roulette")
m.execute('bossbar add roulette "🎲 Spinning the Roulette..."')
#m.execute('bossbar add roulette "🎲 The Roulette is Spinning..."')
#m.execute('bossbar add roulette "🎲 Who will it be?"')
m.execute('bossbar set roulette players @a')

spins = random.randint(10, 15)
result_player = None
result_effect = None

for i in range(spins):
    p = random.choice(players)
    e = random.choice(effects)
    result_player, result_effect = p, e
    
    m.execute('playsound minecraft:block.note_block.hat master @a ~ ~ ~ 1 1.5')

    # Update subtitle, actionbar, and bossbar
    m.execute(f'title @a title ""')
    m.execute(f'title @a subtitle "▶ {p} × {e}"')
    m.execute(f'title @a actionbar "▶ {p} × {e}"')
    m.execute(f'bossbar set roulette name "🎲 {p} × {e}"')
    
    # Slow down for the last 3 spins
    if i >= spins - 3:
        time.sleep(0.5)
    else:
        time.sleep(0.25)

# Show final result
m.execute(f'title @a title ""')
m.execute(f'title @a subtitle "★ {result_player} × {result_effect} ★"')
m.execute(f'title @a actionbar "★ {result_player} × {result_effect} ★"')
m.execute(f'bossbar set roulette name "★ {result_player} × {result_effect} ★"')

# Send chat message
m.execute(f'tellraw @a {{"text":"🎲 Result: {result_player} × {result_effect} ","color":"aqua"}}')

# Apply the effect
apply_effect(result_player, result_effect)
