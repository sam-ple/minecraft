import minescript as m
import time

# =========================
# 設定
# =========================
# CYCLE_TIME = 120  # 秒
CYCLE_TIME = 10  # 秒

# =========================
# 初期設定
# =========================

m.execute("time set day")
# m.execute("gamerule doDaylightCycle false")
m.execute("gamerule send_command_feedback false")

# bossbar作成
m.execute("bossbar remove cycle")
m.execute('bossbar add cycle "昼夜サイクル"')
m.execute(f"bossbar set cycle max {CYCLE_TIME}")
m.execute("bossbar set cycle players @a")
m.execute("bossbar set cycle color yellow")

is_day = True

print("Day/Night Cycle Started")

# =========================
# メインループ
# =========================

while True:

    for t in range(CYCLE_TIME, -1, -1):

        # 分:秒
        m1 = t // 60
        s1 = t % 60
        time_str = f"{m1}:{s1:02d}"

        if is_day:
            title = f"夜まであと {time_str}"
        else:
            title = f"昼まであと {time_str}"

        # ボスバー更新
        m.execute(f'bossbar set cycle name "{title}"')
        m.execute(f"bossbar set cycle value {t}")

        time.sleep(1)

    # =========================
    # 切り替え
    # =========================

    if is_day:

        m.execute("time set night")
        m.execute('title @a actionbar {"text":"夜になりました","color":"dark_blue"}')

        # 夜trigger
        # m.execute("scoreboard players set #night trigger 1")

    else:

        m.execute("time set day")
        m.execute('title @a actionbar {"text":"昼になりました","color":"yellow"}')

        # 昼trigger
        # m.execute("scoreboard players set #day trigger 1")

    is_day = not is_day
