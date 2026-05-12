import minescript as m
import random, time

# ==============================
# 🔧 設定項目
# ==============================
ROULETTE_INTERVAL = 180   # ルーレット間隔（秒）→ 3分
DEFAULT_EFFECT_DURATION = 60  # 効果の基本継続時間（秒）

players = ["crocadooo", "sampleeeeeee", "saaample", "Everyone"]
effects = ["💣 TNT at feet", "👼 Creative Mode", "🩸 Half Heart", "❤️ Full Health", "None"]
"""足元TNT、足元ランダム鉱石、歩くとゾンビ召喚、クリエイティブモード、体力半分、無敵化、ネザライト防具一式を付与"""

# ==============================
# 💣 効果系関数
# ==============================

def effect_tnt(target, duration=DEFAULT_EFFECT_DURATION):
    """攻撃されたら足元に着火TNTを出す（ダメージトラップ）"""
    m.echo(f"💣 {target} にTNT効果を付与 ({duration}s)")
    m.execute(f"execute as {target} at @s run summon tnt ~ ~-1 ~ {{Fuse:60}}")
    # TNTは即時召喚のみ（常時は別スクリプトに分ける）
    time.sleep(duration)
    reset(target)

def effect_creative(target, duration=DEFAULT_EFFECT_DURATION):
    """クリエイティブモード付与"""
    m.echo(f"👼 {target} をクリエイティブに ({duration}s)")
    m.execute(f"gamemode creative {target}")
    time.sleep(duration)
    reset(target)

def effect_half_heart(target, duration=DEFAULT_EFFECT_DURATION):
    """ハート半分"""
    m.echo(f"🩸 {target} の体力を半分に ({duration}s)")
    m.execute(f"attribute {target} minecraft:max_health base set 1")
    time.sleep(duration)
    reset(target)

def effect_full_health(target, duration=DEFAULT_EFFECT_DURATION):
    """体力2倍"""
    m.echo(f"❤️ {target} の体力を2倍に ({duration}s)")
    m.execute(f"attribute {target} minecraft:max_health base set 40")
    time.sleep(duration)
    reset(target)


# ==============================
# ♻️ リセット
# ==============================
def reset(target="@a"):
    """全ての効果をリセット"""
    m.echo(f"🔄 {target} の状態をリセット")
    m.execute(f"gamemode survival {target}")
    m.execute(f"attribute {target} minecraft:max_health base set 20")
    m.execute(f"effect clear {target}")
    m.execute(f"effect give {target} minecraft:instant_health 1 1 true")


# ==============================
# 🎰 ルーレット処理
# ==============================
def spin_roulette():
    """1回分のルーレット演出と効果付与"""
    m.execute("bossbar remove roulette")
    m.execute('bossbar add roulette "🎲 Spinning the Roulette..."')
    m.execute('bossbar set roulette players @a')

    spins = random.randint(10, 15)
    result_player, result_effect = None, None

    for i in range(spins):
        p = random.choice(players)
        e = random.choice(effects)
        result_player, result_effect = p, e

        m.execute('playsound minecraft:block.note_block.hat master @a ~ ~ ~ 1 1.5')
        m.execute(f'title @a title ""')
        m.execute(f'title @a subtitle "▶ {p} × {e}"')
        m.execute(f'title @a actionbar "▶ {p} × {e}"')
        m.execute(f'bossbar set roulette name "🎲 {p} × {e}"')

        time.sleep(0.25 if i < spins - 3 else 0.5)

    # 結果発表
    m.execute(f'title @a subtitle "★ {result_player} × {result_effect} ★"')
    m.execute(f'bossbar set roulette name "★ {result_player} × {result_effect} ★"')
    m.execute(f'tellraw @a {{"text":"🎲 Result: {result_player} × {result_effect}","color":"aqua"}}')

    target = "@a" if result_player == "Everyone" else result_player

    # 効果適用
    if "TNT" in result_effect:
        effect_tnt(target, 10)
    elif "Creative" in result_effect:
        effect_creative(target, 30)
    elif "Half Heart" in result_effect:
        effect_half_heart(target, 45)
    elif "Full Health" in result_effect:
        effect_full_health(target, 60)
    else:
        reset(target)


# ==============================
# 🕹 メインループ
# ==============================
m.echo("🎰 自動ルーレット開始！")
reset()

while True:
    spin_roulette()
    m.echo(f"⏳ 次のルーレットまで {ROULETTE_INTERVAL} 秒待機...")
    time.sleep(ROULETTE_INTERVAL)
