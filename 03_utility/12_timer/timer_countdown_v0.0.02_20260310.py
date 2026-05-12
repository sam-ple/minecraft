import minescript as m
import sys
import time

BOSSBAR_ID = "timer"

# ------------------------
# 秒数取得
# ------------------------

if len(sys.argv) > 1:
    try:
        num = int(sys.argv[1])
    except:
        m.echo("❌ timer <seconds>")
        sys.exit()
else:
    num = 300

# ------------------------
# 既存Bossbar削除
# ------------------------

m.execute(f"bossbar remove {BOSSBAR_ID}")

# ------------------------
# Bossbar作成
# ------------------------

m.execute(f'bossbar add {BOSSBAR_ID} "Timer"')
m.execute(f'bossbar set {BOSSBAR_ID} color blue')
m.execute(f'bossbar set {BOSSBAR_ID} max {num}')
m.execute(f'bossbar set {BOSSBAR_ID} value {num}')
m.execute(f'bossbar set {BOSSBAR_ID} players @a')

m.echo(f"⏱ Timer start ({num}s)")

# ------------------------
# カウントダウン
# ------------------------

for t in range(num, 0, -1):

    minutes = t // 60
    seconds = t % 60

    text = f"{minutes:02d}:{seconds:02d}"

    m.execute(f'bossbar set {BOSSBAR_ID} name "{text}"')
    m.execute(f'bossbar set {BOSSBAR_ID} value {t}')

    time.sleep(1)

# ------------------------
# 終了
# ------------------------

m.execute(f"bossbar remove {BOSSBAR_ID}")

m.execute('title @a title "Time Up!"')
m.echo("⏰ Timer finished")
