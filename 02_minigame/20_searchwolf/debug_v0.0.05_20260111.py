from time import sleep
from minescript import echo, player_get_targeted_entity

echo("🧪 Wolf NBT dump started")

last_uuid = None

while True:
    t = player_get_targeted_entity(max_distance=20, nbt=True)

    if t and t.type == "entity.minecraft.wolf":
        if t.uuid != last_uuid:
            last_uuid = t.uuid
            echo("🐺 ===== WOLF NBT START =====")
            echo(t.nbt)
            echo("🐺 ===== WOLF NBT END =====")

    else:
        last_uuid = None

    sleep(0.3)
