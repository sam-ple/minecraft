import minescript as m
from minescript import EventQueue, EventType
import random
import math

# m.execute("time set night")

# # north

# # ==================================================
# # skeleton (x+1 z-5) 
# # ==================================================

# m.execute("summon minecraft:skeleton ~1 ~ ~-5 {NoAI:1b,PersistenceRequired:1b,Health:2f}")
# #Health:1f / Health:3f

# # ==================================================
# # villager (x-1 z-5)
# # ==================================================
# # https://minecraft-blog.net/summon-villager-command-generator/

# m.execute('/summon villager ~-1 ~ ~-5 {"VillagerData":{"level":5,"profession":"farmer","type":"plains"},"Silent":true,"Invulnerable":true,"NoAI":true,"Offers":{"Recipes":[{"buy":{"id":"emerald","count":1},"sell":{"id":"snowball","count":1},"maxUses":9999}]}}')

# ── 設定 ──
EMERALD_RATE = 0.3  # 30%の確率でエメラルド
eq = EventQueue()
eq.register_damage_listener()  # DamageEventをリッスン

m.echo("⚡ Skeleton Emerald Drop Script Started")

dead_skeletons = set()

# 自然ダメージ系（環境）
ENVIRONMENTAL_SOURCES = {
    "fall", "drown", "lava", "fire", "cactus", "lightning", "starve",
    "suffocate", "explosion", "cramming", "freeze", "sweet_berry_bush", "magic"
}

# ── ユーティリティ ──
def resolve_entity(uuid):
    """UUIDからEntityDataを返す（Player優先）"""
    if not uuid:
        return None
    players_list = m.players(uuid=uuid)
    if players_list:
        return players_list[0]
    entities_list = m.entities(uuid=uuid)
    if entities_list:
        return entities_list[0]
    return None

def format_name(ent):
    """名前＋種別"""
    if ent is None:
        return "Unknown", "?"
    if getattr(ent, "local", False):
        return ent.name, "Player"
    elif "minecraft:" in getattr(ent, "type", ""):
        return ent.type.split(":")[-1].replace("_", " ").title(), "Mob"
    else:
        return getattr(ent, "name", None) or getattr(ent, "type", "?"), "Entity"

def get_xyz(pos):
    if pos is None:
        return None
    if isinstance(pos, (list, tuple)) and len(pos) >= 3:
        return pos[0], pos[1], pos[2]
    if all(hasattr(pos, k) for k in ("x", "y", "z")):
        return pos.x, pos.y, pos.z
    return None

def distance(pos1, pos2):
    a = get_xyz(pos1)
    b = get_xyz(pos2)
    if not a or not b:
        return None
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

# ── メインループ ──
while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    victim = resolve_entity(event.entity_uuid)
    attacker = resolve_entity(event.cause_uuid)

    # スケルトンだけ処理
    if not victim or "skeleton" not in getattr(victim, "type", "").lower():
        continue

    # まだ倒されていない場合のみ
    if getattr(victim, "health", 1) > 0:
        continue

    if victim.uuid in dead_skeletons:
        continue
    dead_skeletons.add(victim.uuid)

    # 攻撃者がプレイヤーであること
    if not attacker or getattr(attacker, "local", False) is False:
        continue

    # ランダム判定
    if random.random() < EMERALD_RATE:
        m.execute(f"give {attacker.name} minecraft:emerald 1")
        m.echo(f"💎 {attacker.name} received an emerald for killing a skeleton!")
