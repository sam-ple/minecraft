from time import sleep, time
from minescript import echo, player_get_targeted_entity

CHECK_INTERVAL = 0.1
REQUIRED_LOOK_TIME = 1.0
MISS_DECAY = 0.15   # Noneが出た時に減らす秒数

current_uuid = None
look_time = 0.0

echo("🎯 Wolf gaze debug started")
echo("👀 Look at ONE wolf until confirmed")

while True:
    start = time()
    t = player_get_targeted_entity(max_distance=20)

    if t and t.type == "entity.minecraft.wolf":
        # 新しい狼を見た
        if t.uuid != current_uuid:
            current_uuid = t.uuid
            look_time = 0.0
            echo(f"🔁 New wolf locked: {current_uuid}")

        look_time += CHECK_INTERVAL
        echo(f"👀 Looking: {t.uuid} | {look_time:.2f}s")

        if look_time >= REQUIRED_LOOK_TIME:
            echo("✅ LOOK CONFIRMED (1 second)")
            look_time = 0.0
            current_uuid = None
            sleep(0.5)

    else:
        # 一瞬の視線ロストは減衰のみ
        if look_time > 0:
            look_time = max(0.0, look_time - MISS_DECAY)

    elapsed = time() - start
    sleep(max(0, CHECK_INTERVAL - elapsed))
