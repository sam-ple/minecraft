import minescript as m
import random, time

players = ["test1", "test2", "test3", "全員"]
effects = ["足元TNT", "ハート0.5", "ハート20", "クリエイティブモード", "無し"]

def apply_effect(player, effect):
    target = "@a" if player == "全員" else player
    
    if effect == "足元TNT":
        m.execute(f"execute as {target} at @s run summon tnt ~ ~ ~")
    elif effect == "ハート0.5":
        m.execute(f"/attribute {target} minecraft:max_health base set 1")
    elif effect == "ハート20":
        m.execute(f"/attribute {target} minecraft:max_health base set 40")
    elif effect == "クリエイティブモード":
        m.execute(f"gamemode creative {target}")
    elif effect == "無し":
        pass

# ボスバー初期化
m.execute('bossbar add roulette "🎲 ルーレット中..."')
m.execute('bossbar set roulette players @a')

spins = random.randint(10, 15)
result_player = None
result_effect = None

for i in range(spins):
    p = random.choice(players)
    e = random.choice(effects)
    result_player, result_effect = p, e
    
    # サブタイトル・アクションバー・ボスバー更新
    m.execute(f'title @a title ""')
    m.execute(f'title @a subtitle "▶ {p} × {e}"')
    m.execute(f'title @a actionbar "▶ {p} × {e}"')
    m.execute(f'bossbar set roulette name "🎲 {p} × {e}"')
    
    # 最後の3回だけスローダウン
    if i >= spins - 3:
        time.sleep(0.5)
    else:
        time.sleep(0.25)

# 最終結果表示
m.execute(f'title @a title ""')
m.execute(f'title @a subtitle "★ {result_player} × {result_effect} ★"')
m.execute(f'title @a actionbar "★ {result_player} × {result_effect} ★"')
m.execute(f'bossbar set roulette name "★ {result_player} × {result_effect} ★"')

# チャット通知
m.execute(f'tellraw @a {{"text":"🎲 結果: {result_player} × {result_effect} ","color":"aqua"}}')

# 効果適用
apply_effect(result_player, result_effect)
