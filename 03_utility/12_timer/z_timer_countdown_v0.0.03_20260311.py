import minescript as m
import sys
import time
from minescript import EventQueue, EventType
from system.lib.minescript import job_info, execute

# ==================================================
# CONFIG
# ==================================================

JOB_NAME = "timer"

DEFAULT_TIME = 600
ENABLE_EFFECT = 1

BOSSBAR_ID = "timer"

COLOR_DEFAULT = "blue"
COLOR_60 = "yellow"
COLOR_30 = "red"
COLOR_PAUSE = "purple"

SOUND_COUNT = "minecraft:block.note_block.pling"
SOUND_FINAL = "minecraft:block.note_block.bell"
SOUND_START = "minecraft:entity.player.levelup"
SOUND_FINISH = "minecraft:entity.firework_rocket.launch"

# ==================================================
# util
# ==================================================

def cmd(c):
    m.execute(c)

def play(sound, pitch=1):
    cmd(f"playsound {sound} master @a ~ ~ ~ 1 {pitch}")

def format_time(t):

    hours = t // 3600
    minutes = (t % 3600) // 60
    seconds = t % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def update_color(t):

    if t <= 30:
        cmd(f"bossbar set {BOSSBAR_ID} color {COLOR_30}")
    elif t <= 60:
        cmd(f"bossbar set {BOSSBAR_ID} color {COLOR_60}")
    else:
        cmd(f"bossbar set {BOSSBAR_ID} color {COLOR_DEFAULT}")

def kill_timer():

    cmd(f"bossbar remove {BOSSBAR_ID}")

    jobs = job_info()

    for job in jobs:
        if job.command.startswith(JOB_NAME):
            execute(f"\\killjob {job.job_id}")

# ==================================================
# 秒数取得
# ==================================================

if len(sys.argv) > 1:
    try:
        num = int(sys.argv[1])
    except:
        num = DEFAULT_TIME
else:
    num = DEFAULT_TIME

# ==================================================
# bossbar reset
# ==================================================

cmd(f"bossbar remove {BOSSBAR_ID}")

# ==================================================
# bossbar create
# ==================================================

cmd(f'bossbar add {BOSSBAR_ID} "Timer"')
cmd(f'bossbar set {BOSSBAR_ID} color {COLOR_DEFAULT}')
cmd(f'bossbar set {BOSSBAR_ID} max {num}')
cmd(f'bossbar set {BOSSBAR_ID} value {num}')
cmd(f'bossbar set {BOSSBAR_ID} players @a')

# ==================================================
# countdown effect
# ==================================================

if ENABLE_EFFECT:

    for t in [3,2,1]:
        cmd(f'title @a title "{t}"')
        play(SOUND_COUNT)
        time.sleep(1)

    cmd('title @a title "START!"')
    play(SOUND_START)

m.echo(f"⏱ Timer start ({num}s)")

# ==================================================
# chat listener
# ==================================================

eq = EventQueue()
eq.register_chat_listener()

# ==================================================
# timer state
# ==================================================

paused = False
t = num

# ==================================================
# timer loop
# ==================================================

while t > 0:

    # ----------------------------
    # chat command check
    # ----------------------------

    try:
        event = eq.get(timeout=0.05)

        if event.type == EventType.CHAT:

            msg = event.message.strip()

            # ----- stop -----

            if msg == "--stop":

                kill_timer()
                m.echo("⏹ Timer stopped")
                sys.exit()

            # ----- pause -----

            if msg == "--pause" and not paused:

                paused = True
                cmd(f'bossbar set {BOSSBAR_ID} color {COLOR_PAUSE}')
                m.echo("⏸ Timer paused")

            # ----- resume -----

            if msg == "--resume" and paused:

                paused = False
                update_color(t)
                m.echo("▶ Timer resumed")

    except:
        pass

    # ----------------------------
    # pause状態
    # ----------------------------

    if paused:
        time.sleep(0.5)
        continue

    # ----------------------------
    # bossbar update
    # ----------------------------

    text = format_time(t)

    # cmd(f'bossbar set {BOSSBAR_ID} name "{text}"')
    cmd(f'bossbar set {BOSSBAR_ID} value {t}')

    # ----------------------------
    # color change
    # ----------------------------

    if t == 60 or t == 30:
        update_color(t)

    # ----------------------------
    # effects
    # ----------------------------

    if ENABLE_EFFECT:

        if 1 <= t <= 5:
            cmd(f'title @a title "{t}"')
            play(SOUND_FINAL,1.5)
        # ----------------------------
        # tick
        # ----------------------------

        time.sleep(1)
        t -= 1

# ==================================================
# finish
# ==================================================

cmd(f"bossbar remove {BOSSBAR_ID}")

if ENABLE_EFFECT:
    cmd('title @a title "FINISH!"')
    play(SOUND_FINISH)

m.echo("🏁 Timer finished")
