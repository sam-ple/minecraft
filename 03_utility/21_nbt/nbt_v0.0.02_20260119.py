import json
import time
import os
from datetime import datetime, timezone, timedelta

from minescript import player_get_targeted_entity

OUT_PATH = "minescript/data/nbt.jsonl"
INTERVAL = 5.0  # 秒（短め）
JST = timezone(timedelta(hours=9))

last_uuid = None  # 直前に保存したMobのUUID


def ensure_output_file():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    if not os.path.exists(OUT_PATH):
        open(OUT_PATH, "w", encoding="utf-8").close()


def dump_target_nbt():
    global last_uuid

    entity = player_get_targeted_entity(20, nbt=True)
    if entity is None:
        return

    if not hasattr(entity, "nbt") or entity.nbt is None:
        return

    # UUIDが同じならスキップ
    if entity.uuid == last_uuid:
        return

    last_uuid = entity.uuid

    data = {
        "timestamp": datetime.now(JST).isoformat(),
        "type": entity.type,
        "uuid": entity.uuid,
        "nbt": entity.nbt,
    }

    with open(OUT_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    print(f"[NBT] Logged {entity.type} ({entity.uuid})")


print("[NBT] Target NBT logger started (UUID change trigger)")
ensure_output_file()

while True:
    try:
        dump_target_nbt()
        time.sleep(INTERVAL)
    except Exception as e:
        print("[NBT] Error:", e)
        time.sleep(2)
