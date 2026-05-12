import minescript as m
import random, time

players = ["crocadooo", "sampleeeeeee", "saaample"]
roles = ["Giant", "Tiny", "Warrior"]

ROLE_EFFECTS = {
    "Giant": {"scale": 10, "effects": []},
    "Tiny": {"scale": 0.5, "effects": []},
    "Warrior": {"scale": 1.0, "effects": ["strength", "speed"]}
}

DURATION = 15  # 効果持続時間（秒）

# 既存タグをリセット
for p in players:
    m.execute(f'tag {p} remove Giant')
    m.execute(f'tag {p} remove Tiny')
    m.execute(f'tag {p} remove Warrior')

# ランダムに役職を付与
for p in players:
    role = random.choice(roles)
    m.execute(f'tag {p} add {role}')
    m.echo(f"{p} → {role}")

    # サイズ変更
    scale = ROLE_EFFECTS[role]["scale"]
    m.execute(f'execute as {p} run attribute @s minecraft:scale base set {scale}')

    # 武器効果（ポーションなど）
    for effect in ROLE_EFFECTS[role]["effects"]:
        m.execute(f'effect give {p} minecraft:{effect} {DURATION} 1 true')

    # DURATION 秒後にサイズ・効果を元に戻す場合
    time.sleep(DURATION)
    m.execute(f'execute as {p} run attribute @s minecraft:scale base set 1.0')
    for effect in ROLE_EFFECTS[role]["effects"]:
        m.execute(f'effect clear {p} minecraft:{effect}')

m.echo("✅ Roles assigned and effects applied!")
