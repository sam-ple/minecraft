from time import sleep
from minescript import echo, player_get_targeted_entity, execute

echo("🧪 Wolf VARIANT (execute-based) debug started")

last_uuid = None

def get_variant_by_execute(uuid):
    """
    /data get entity <uuid> variant
    の結果をチャットから拾う
    """
    execute(f'data get entity {uuid} variant')

while True:
    t = player_get_targeted_entity(max_distance=20)

    if t and t.type == "entity.minecraft.wolf":
        if t.uuid != last_uuid:
            last_uuid = t.uuid

            echo("🐺 ===== WOLF DETECTED =====")
            echo(f"UUID : {t.uuid}")
            echo("➡ querying variant via /data get …")

            get_variant_by_execute(t.uuid)

            echo("🐺 =========================")

    else:
        last_uuid = None

    sleep(0.4)
