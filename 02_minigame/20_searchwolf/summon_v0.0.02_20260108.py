import minescript as m
import time
import math

# ==================================================
# Wolf variant list (Minecraft 1.20+)
# ==================================================
WOLF_VARIANTS = [
    "pale",
    "woods",
    "ashen",
    "black",
    "chestnut",
    "rusty",
    "spotted",
    "striped",
    "snowy",
    "classic",
    "big",
    "grumpy"
]

# ==================================================
# Summon all wolf variants in a horizontal line
# (Facing direction of the player)
# ==================================================
def summon_all_wolves():
    m.echo("🐺 Summoning all wolf variants in a line...")

    # Player position and orientation
    px, py, pz = m.player_position()
    yaw, pitch = m.player_orientation()

    # Minecraft yaw:
    #   0   = South
    #   90  = West
    #   180 = North
    #   270 = East
    yaw_rad = math.radians(yaw)

    # Forward direction vector
    forward_x = -math.sin(yaw_rad)
    forward_z =  math.cos(yaw_rad)

    # Right direction vector
    right_x =  math.cos(yaw_rad)
    right_z =  math.sin(yaw_rad)

    # Base position: 3 blocks in front of the player
    base_x = px + forward_x * 3
    base_y = py
    base_z = pz + forward_z * 3

    spacing = 2.0
    start_offset = -(len(WOLF_VARIANTS) - 1) / 2

    # ==================================================
    # Summon each wolf variant
    # ==================================================
    for i, variant in enumerate(WOLF_VARIANTS):
        offset = (start_offset + i) * spacing

        x = base_x + right_x * offset
        z = base_z + right_z * offset

        # Wolf NBT data
        nbt = (
            f'{{'
            f'Health:8.0f,'
            f'NoAI:1b,'
            f'Sitting:1b,'
            f'Silent:1b,'
            f'CollarColor:14b,'
            f'variant:"minecraft:{variant}",'
            f'sound_variant:"minecraft:{variant}"'
            f'}}'
        )

        m.execute(f'summon wolf {x:.2f} {base_y:.2f} {z:.2f} {nbt}')
        m.echo(f"🐺 Summoned wolf: {variant}")
        time.sleep(0.3)

    m.echo("✅ All wolf variants summoned successfully!")

# ==================================================
# Entry point
# ==================================================
summon_all_wolves()
