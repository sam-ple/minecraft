from time import sleep
from minescript import echo, player_get_targeted_entity

echo("🔍 Target Debug started")
echo("🎯 Look at an entity")

while True:
    t = player_get_targeted_entity(max_distance=20, nbt=True)

    if not t:
        echo("TARGET: None")
    else:
        echo(
            f"TARGET: type={t.type} | "
            f"uuid={t.uuid} | "
            f"nbt={'yes' if isinstance(t.nbt, str) else 'no'}"
        )

        if t.type == "minecraft:wolf":
            echo("🐺 >>> THIS IS A WOLF <<<")

    sleep(0.3)
