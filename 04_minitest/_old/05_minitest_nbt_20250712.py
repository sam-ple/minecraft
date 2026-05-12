
import minescript as m
import time
import json
import math
from sys import argv, exit

def give_book():
    player = m.player_name()
    # NBT string for the book content
    nbt = (
        'written_book_content={'
        'pages:[[["test"]]],'
        'title:TestBook,'
        'author:sam-ple'
        '}'
    )
    cmd = f'give {player} written_book[{nbt}]'
    m.execute(cmd)
    m.echo("✅ Given the book")

def place_sign():
    x, y, z = map(math.floor, m.player_position())
    m.execute(f'setblock {x} {y} {z} minecraft:pale_oak_sign[rotation=0]')

    sign_data = {
        "front_text": {
            "color": "black",
            "has_glowing_text": 0,
            "messages": [
                {"text": ""},
                {"text": "Test"},
                {"text": ""},
                {"text": ""}
            ]
        }
    }
    sign_data_str = json.dumps(sign_data, separators=(',', ':'))
    m.execute(f'data merge block {x} {y} {z} {sign_data_str}')
    m.echo("✅ Placed the sign and set NBT")

def summon_armorstand():
    x, y, z = map(math.floor, m.player_position())

    nbt = {
        "ShowArms": 1,
        "Invisible": 0,
        "Small": 0,
        "NoBasePlate": 0,
        "equipment": {
            "mainhand": {"id": "minecraft:golden_sword", "count": 1},
            "head": {"id": "minecraft:piglin_head", "count": 1},
            "chest": {"id": "minecraft:golden_chestplate", "count": 1},
            "legs": {"id": "minecraft:golden_leggings", "count": 1},
            "feet": {"id": "minecraft:golden_boots", "count": 1}
        }
    }
    nbt_str = json.dumps(nbt, separators=(',', ':'))
    m.execute(f'summon armor_stand {x} {y} {z} {nbt_str}')
    m.echo("✅ Summoned the armor stand")

def main():
    if len(argv) < 2:
        m.echo("Please specify a command: sign, armorstand, book, all")
        exit(1)

    arg1 = argv[1].lower()

    if arg1 == "sign":
        place_sign()
    elif arg1 == "armorstand":
        summon_armorstand()
    elif arg1 == "book":
        give_book()
    elif arg1 == "all":
        give_book()
        time.sleep(0.5)
        place_sign()
        time.sleep(0.5)
        summon_armorstand()
    else:
        m.echo(f"Unsupported command: {arg1}")

if __name__ == "__main__":
    main()
