import minescript as m
import time
import math

def place_tnt_underfoot():
    while True:
        x, y, z = m.player_position()
        x, y, z = math.floor(x), math.floor(y), math.floor(z)

        block_below = m.getblock(x, y-1, z)

        TARGET_BLOCKS = ["minecraft:dirt", "minecraft:grass_block"]
#        if block_below in TARGET_BLOCKS:
        if any(target in block_below for target in TARGET_BLOCKS):
            m.execute(f"setblock {x} {y-1} {z} minecraft:tnt")
            m.echo(f"TNT placed underfoot at {x},{y-1},{z}")

        time.sleep(0.1)  # 0.1秒ごとにチェック

if __name__ == "__main__":
    m.echo("TNT underfoot activated!")
    place_tnt_underfoot()
