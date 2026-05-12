import minescript as m
from minescript import EventQueue, EventType
import re, time
from datetime import datetime
import shutil
import random
import json
from queue import Empty

"""
Memo:
"""

m.execute("gamerule sendCommandFeedback false")
m.execute("gamerule logAdminCommands false")
m.execute("difficulty peaceful")
m.execute("time set day")
m.execute("weather clear")

# --- ヘルパー関数 ---
def m_chat(msg: str):
    """全員に通知"""
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": "green", "bold": True})}')

def m_echo(msg: str):
    """crocadooo にだけ黄色で通知"""
#    m.execute(f'tellraw crocadooo {json.dumps({"text": msg, "color": "yellow"})}')
    m.execute(f'tellraw {m.player_name()} {json.dumps({"text": msg, "color": "yellow"})}')

# --- 初期設定 ---
GAME_DURATION = 600  # 10 minutes
START_POSITIONS = [
    "-30 70 -92",
    # ... 合計20個くらい
]

def get_random_start_pos():
    return random.choice(START_POSITIONS)

# ロビー（終了時の待機場所）
LOBBY_POS = "7 91 6"
m.execute(f"/setworldspawn {LOBBY_POS}")

player_points = {}
player_advancements = {}
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")
eq = EventQueue()
eq.register_chat_listener()
m_echo("Chat listener ready!")

game_active = False
game_start_time = None

# --- ログ管理 ---
adv_log_file = "adv_output.txt"

def save_adv_text(player_name, advancement_name):
    """進捗達成をプレイヤーごとに1行で時間付きで記録"""
    now = int(time.time())
    elapsed = int(now - game_start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    timestamp = f"{minutes:02d}:{seconds:02d}"

    try:
        with open(adv_log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    lines_dict = {}
    for line in lines:
        line = line.strip()
        if not line: continue
        pname, rest = line.split(":", 1)
        lines_dict[pname] = rest.strip()

    prev = lines_dict.get(player_name, "")
    new_entry = f"{timestamp} {advancement_name}"
    if prev:
        new_entry = prev + " | " + new_entry
    lines_dict[player_name] = new_entry

    with open(adv_log_file, "w", encoding="utf-8") as f:
        for pname, advs in lines_dict.items():
            f.write(f"{pname}: {advs}\n")

# --- ボスバー更新キャッシュ ---
last_remaining = None
last_name = None

current_start_pos = None

# --- ゲーム開始 ---
def start_game():
    global game_active, game_start_time, player_points, player_advancements
    global last_remaining, last_name, current_start_pos
    
    last_remaining = None
    last_name = None
    current_start_pos = get_random_start_pos()

    try:
        open(adv_log_file, "w", encoding="utf-8").close()
        m_echo("adv_output.txt reset for new game")
    except Exception as e:
        m_echo(f"Failed to reset adv_output.txt: {e}")

    m.execute("scoreboard objectives remove AdvPoints")
    m.execute("scoreboard objectives add AdvPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar AdvPoints")

    m.execute("/advancement revoke @a everything")
    m.execute("/clear @a")

    player_points = {}
    player_advancements = {}
    game_active = True
    
    m.execute('bossbar add timer "Countdown"')
    m.execute('bossbar set timer color blue')
    m.execute(f'bossbar set timer max {GAME_DURATION}')
    m.execute(f'bossbar set timer value {GAME_DURATION}')
    m.execute('bossbar set timer players @a')

    m.execute(f'/spawnpoint @a {current_start_pos}')
    m.execute(f'/tp @a {current_start_pos}')

    # ゲーム開始時に全員を回復
    m.execute("/effect give @a minecraft:instant_health 1 1 true")  # ハート回復
    m.execute("/effect give @a minecraft:saturation 1 1 true")     # 空腹ゲージ回復

    m.execute("difficulty normal")
    m.execute("time set day")
    m.execute("weather clear")

    m.execute('/title @a title {"text":"Ready...","color":"aqua","bold":true}')
    time.sleep(1)
    for count in ["3","2","1"]:
        m.execute(f'/title @a title {{"text":"{count}","color":"aqua","bold":true}}')
        m.execute('/playsound minecraft:block.note_block.pling master @a')
        time.sleep(1)

    # ここで開始時刻をセット
    game_start_time = time.time()

    # カウントダウン終了でサバイバルに
    m.execute("/gamemode survival @a")

    m.execute('/title @a title {"text":"Game Start!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.player.levelup master @a')
    time.sleep(0.5)

    m_chat(f"Game Started at {current_start_pos}!")

# --- ゲーム終了 ---
def end_game():
    global game_active, sorted_players
    game_active = False

    sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
    colors = ["gold", "green", "aqua"]  # 上位3位だけ色付き

    m.execute('/title @a title {"text":"Game End!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.player.levelup master @a')

    # ゲーム終了時に全員アドベンチャーモード
    m.execute("/gamemode adventure @a")
    m.execute("difficulty peaceful")

    m.execute(f"/spawnpoint @a {LOBBY_POS}")
    m.execute(f"/tp @a {LOBBY_POS}")

    def rank_suffix(n: int) -> str:
        if n % 100 in (11, 12, 13):
            return "th"
        elif n % 10 == 1:
            return "st"
        elif n % 10 == 2:
            return "nd"
        elif n % 10 == 3:
            return "rd"
        else:
            return "th"

    # ランキング全体のメッセージを作成
    lines = []

    # 最初の空行
    lines.append({"text": "\n"})

    for i, (player, pts) in enumerate(sorted_players):
        rank = f"{i+1}{rank_suffix(i+1)}"
        color = colors[i] if i < len(colors) else "white"
        bold = True if i < 3 else False
        lines.append({"text": f"{rank}: {player} ({pts} pts)\n", "color": color, "bold": bold})

    # 最後の空行
    lines.append({"text": "\n"})

    msg = {"text": "", "extra": lines}
    m.execute(f'tellraw @a {json.dumps(msg)}')

    m.execute('bossbar remove timer')

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"adv_output_{now}.txt"
    try:
        shutil.copy(adv_log_file, backup_file)
        m_echo(f"Backup saved as {backup_file}")
    except FileNotFoundError:
        m_echo("No adv_output.txt to backup")

# --- ボスバー更新（メインループ内） ---
last_bossbar_update = 0
BOSSBAR_INTERVAL = 1  # 1秒ごとに更新

# --- メインループ ---
while True:
    try:
        event = eq.get(timeout=0.05)
    except Empty:
        event = None  # イベントがなかったら None にする

    if event and event.type == EventType.CHAT:
        msg = event.message
        if msg.startswith("<") and ">" in msg:
            player_name, content = msg[1:].split(">", 1)
            content = content.strip()

            if content.startswith("--"):
                if game_active and not (content.startswith("--adv") or content in ["--stop", "--help","--status","--tp","--home"]):
                    m_chat("Game in progress! Only --adv, --help, --stop, --tp, --home are available.")
                    continue

                if content == "--start" and not game_active:
                    start_game()
                elif content == "--stop" and game_active:
                    end_game()
                    m_chat("Game forcibly stopped.")
                elif content.startswith("--settime"):
                    parts = content.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        GAME_DURATION = int(parts[1])
                        mins = GAME_DURATION // 60
                        secs = GAME_DURATION % 60
                        time_str = f"{mins:02d}:{secs:02d}"
                        m_chat(f"Game duration set to {time_str}")
                    else:
                        m_chat("Usage: --settime <seconds>")
                elif content == "--status":
                    if game_active:
                        elapsed = int(time.time() - game_start_time)
                        remaining = max(GAME_DURATION - elapsed, 0)
                        mins = remaining // 60
                        secs = remaining % 60
                        time_str = f"{mins:02d}:{secs:02d}"
                        m_chat(f"Game in progress! Remaining time: {time_str}")
                    else:
                        mins = GAME_DURATION // 60
                        secs = GAME_DURATION % 60
                        time_str = f"{mins:02d}:{secs:02d}"
                        m_chat(f"No game running. Default duration: {time_str}")
                elif content.startswith("--adv"):
                    parts = content.split()
                    if len(parts) == 2:
                        target = parts[1]
                        try:
                            with open(adv_log_file, "r", encoding="utf-8") as f:
                                lines = f.readlines()
                        except FileNotFoundError:
                            lines = []
                        found = False
                        for line in lines:
                            if line.startswith(target + ":"):
                                found = True
                                m_chat(f"{player_name} requested --adv:\n {line.strip()}")
                        if not found:
                            m_chat(f"{player_name} requested --adv:\n No advancements found for {target}")
                elif content == "--tp":
                    if game_active and current_start_pos:
                        m.execute(f"/tp {player_name} {current_start_pos}")
                        m_chat(f"{player_name} has joined the game area!")
                    else:
                        m_chat("No active game to join.")
                elif content == "--home":
                    m.execute(f"/tp {player_name} {LOBBY_POS}")
                    m_chat(f"{player_name} returned to the lobby.")
                elif content == "--help":
                    help_texts = [
                        {"text": "\n--start : Start the game", "color": "aqua", "bold": True},
                        {"text": "--stop : End the game", "color": "aqua", "bold": True},
                        {"text": "--settime <seconds> : Set game duration", "color": "aqua", "bold": True},
                        {"text": "--status : Check remaining game time", "color": "aqua", "bold": True},
                        {"text": "--adv <player name> : Check player advancements", "color": "aqua", "bold": True},
                        {"text": "--tp : Teleport to the game area", "color": "aqua", "bold": True},
                        {"text": "--home : Return to the lobby", "color": "aqua", "bold": True},
                        {"text": "--help : Show this help message\n", "color": "aqua", "bold": True},
                    ]
                    for line in help_texts:
                        m.execute(f'tellraw @a {json.dumps(line)}')

    current_time = time.time()
    if game_active and current_time - last_bossbar_update >= BOSSBAR_INTERVAL:
        elapsed = int(current_time - game_start_time)
        remaining = max(GAME_DURATION - elapsed, 0)

        # ボスバー更新
        m.execute(f'bossbar set timer value {remaining}')
        mins = remaining // 60
        secs = remaining % 60
        name = f"{mins:02d}:{secs:02d}"
        m.execute(f'bossbar set timer name "{name}"')

        last_bossbar_update = current_time

        # 残り時間が 0 になったらゲーム終了
        if remaining <= 0:
            end_game()
            m_chat("Time's up! Game ended.")

    if game_active and event and event.type == EventType.CHAT:
        msg = event.message.strip()
        match = adv_pattern.match(msg)
        if match:
            player_name, action, advancement_name = match.groups()
            player_points[player_name] = player_points.get(player_name, 0) + 1
            if player_name not in player_advancements:
                player_advancements[player_name] = []
            if advancement_name not in player_advancements[player_name]:
                player_advancements[player_name].append(advancement_name)
            m.execute(f"scoreboard players set {player_name} AdvPoints {player_points[player_name]}")
            m_echo(f"{player_name} earned 1 point for '{advancement_name}'! (Total: {player_points[player_name]})")
            m.execute('/playsound minecraft:block.note_block.chime master @a')
            save_adv_text(player_name, advancement_name)

