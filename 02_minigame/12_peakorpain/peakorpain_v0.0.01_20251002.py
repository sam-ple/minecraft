import minescript as m
import random, time

players = ["test1", "test2", "test3", "全員"]
effects = ["足元TNT", "ハート0.5", "クリエイティブモード", "無し"]

def apply_effect(player, effect):
    """選ばれた効果を適用"""
    target = "@a" if player == "全員" else player
    
    if effect == "足元TNT":
        m.execute(f"execute as {target} at @s run summon tnt ~ ~ ~ {{Fuse:80}}")
    elif effect == "ハート0.5":
        m.execute(f"/attribute {target} minecraft:max_health base set 1")
    elif effect == "クリエイティブモード":
        m.execute(f"gamemode creative {target}")
    elif effect == "無し":
        pass  # 何もしない

# ルーレット演出（10〜15回ランダムに切り替え）
spins = random.randint(10, 15)
result_player = None
result_effect = None

for i in range(spins):
    p = random.choice(players)
    e = random.choice(effects)
    # タイトルで演出（全員に表示）
    m.execute(f'title @a title "{p} × {e}"')
    result_player, result_effect = p, e
    time.sleep(0.25)

# 最終結果を強調して表示
m.execute(f'title @a title "★ {result_player} × {result_effect} ★"')

# 結果をチャットに通知
m.execute(f'tellraw @a {{"text":"🎲 結果: {result_player} × {result_effect} ","color":"aqua"}}')

# 効果を適用
apply_effect(result_player, result_effect)
