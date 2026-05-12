import minescript as m
import sys
import time
import json
import os
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

STATE_FILE = "minescript/data/timer_state.json"

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

    try:
        cmd(f"bossbar remove {BOSSBAR_ID}")
    except:
        pass

    jobs = job_info()

    for job in jobs:
        if job.command.startswith(JOB_NAME):
            execute(f"\\killjob {job.job_id}")

    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

# ==================================================
# STATE
# ==================================================

def save_state(finish_time, duration):

    os.makedirs("minescript/data", exist_ok=True)

    data = {
        "finish_time": finish_time,
        "duration": duration
    }

    with open(STATE_FILE,"w") as f:
        json.dump(data,f)

def load_state():

    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE) as f:
        return json.load(f)

# ==================================================
# 引数処理
# ==================================================

mode = "start"

if len(sys.argv) > 1:

    if sys.argv[1] == "restart":
        mode = "restart"
    else:
        try:
            num = int(sys.argv[1])
        except:
            num = DEFAULT_TIME
else:
    num = DEFAULT_TIME

# ==================================================
# restart処理
# ==================================================

if mode == "restart":

    state = load_state()

    if not state:
        m.echo("No timer state found.")
        sys.exit()

    finish_time = state["finish_time"]
    duration = state["duration"]

    remaining = int(finish_time - time.time())

    if remaining <= 0:
        m.echo("Timer already finished.")
        kill_timer()
        sys.exit()

    num = remaining

else:

    duration = num
    finish_time = time.time() + num

# ==================================================
# bossbar reset
# ==================================================

try:
    cmd(f"bossbar remove {BOSSBAR_ID}")
except:
    pass

# ==================================================
# bossbar create
# ==================================================

cmd(f'bossbar add {BOSSBAR_ID} "Timer"')
cmd(f'bossbar set {BOSSBAR_ID} color {COLOR_DEFAULT}')
cmd(f'bossbar set {BOSSBAR_ID} max {duration}')
cmd(f'bossbar set {BOSSBAR_ID} value {num}')
cmd(f'bossbar set {BOSSBAR_ID} players @a')

# ==================================================
# countdown（restartではスキップ）
# ==================================================

if ENABLE_EFFECT and mode != "restart":

    for t in [3,2,1]:
        cmd(f'title @a title "{t}"')
        play(SOUND_COUNT)
        time.sleep(1)

    cmd('title @a title "START!"')
    play(SOUND_START)

m.echo(f"⏱ Timer start ({num}s)")

# ==================================================
# state save（restartでは保存済み）
# ==================================================

if mode != "restart":
    save_state(finish_time, duration)

# ==================================================
# chat listener
# ==================================================

eq = EventQueue()
eq.register_chat_listener()

# ==================================================
# timer state
# ==================================================

paused = False
pause_start = None
t = num

# ==================================================
# timer loop
# ==================================================

while t > 0:

    try:
        event = eq.get(timeout=0.05)

        if event.type == EventType.CHAT:

            msg = event.message.strip()

            if msg == "--stop":

                kill_timer()
                m.echo("⏹ Timer stopped")
                sys.exit()

            if msg == "--pause" and not paused:

                paused = True
                pause_start = time.time()

                cmd(f'bossbar set {BOSSBAR_ID} color {COLOR_PAUSE}')
                m.echo("⏸ Timer paused")

            if msg == "--resume" and paused:

                paused = False

                pause_duration = time.time() - pause_start
                finish_time += pause_duration

                save_state(finish_time, duration)

                update_color(t)
                m.echo("▶ Timer resumed")

    except:
        pass

    if paused:
        time.sleep(0.5)
        continue

    text = format_time(t)

    # cmd(f'bossbar set {BOSSBAR_ID} name "{text}"')
    cmd(f'bossbar set {BOSSBAR_ID} value {t}')

    if t == 60 or t == 30:
        update_color(t)

    if ENABLE_EFFECT:

        if 1 <= t <= 5:
            cmd(f'title @a title "{t}"')
            play(SOUND_FINAL,1.5)

    time.sleep(1)
    t -= 1

# ==================================================
# finish
# ==================================================

try:
    cmd(f"bossbar remove {BOSSBAR_ID}")
except:
    pass

if ENABLE_EFFECT:
    cmd('title @a title "FINISH!"')
    play(SOUND_FINISH)

if os.path.exists(STATE_FILE):
    os.remove(STATE_FILE)

m.echo("🏁 Timer finished")