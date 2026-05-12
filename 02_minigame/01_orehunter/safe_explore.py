import minescript as m

# Set game mode to peaceful at the start
m.execute("gamerule difficulty peaceful")

# --- Apply safety effects to player ---

effects = [
    ("minecraft:resistance", 1000000, 4),      # Max damage resistance
    ("minecraft:slow_falling", 1000000, 0),    # No fall damage
    ("minecraft:fire_resistance", 1000000, 0), # Lava/fire protection
    ("minecraft:water_breathing", 1000000, 0), # Breathe underwater
    ("minecraft:night_vision", 1000000, 0),    # See in darkness
]

target = "@p"

for effect, duration, amplifier in effects:
    m.execute(f"/effect give {target} {effect} {duration} {amplifier} true")

# Optional game rules
# m.execute("/gamerule keepInventory true")     # Keep inventory on death

# Optional: Clear effects manually
# m.execute(f"/effect clear {target}")          # Clear all effects