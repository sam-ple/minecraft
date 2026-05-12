import minescript as m
from minescript import EventQueue, EventType
import re, time
from datetime import datetime
import shutil
import random
import json

m.execute("gamerule sendCommandFeedback false")
m.execute("gamerule logAdminCommands false")
# /tellraw @a "test has made the advancement [Diamonds!]"

# --- ヘルパー関数 ---
def m_chat(msg: str):
    """全員に通知"""
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": "white"})}')

def m_echo(msg: str):
    """crocadooo にだけ黄色で通知"""
    m.execute(f'tellraw crocadooo {json.dumps({"text": msg, "color": "yellow"})}')

# --- 初期設定 ---
GAME_DURATION = 600  # 10 minutes
START_POSITIONS = [
    "-30 70 -92",
    # ... 合計20個くらい
]

def get_random_start_pos():
    return random.choice(START_POSITIONS)

# ロビー（終了時の待機場所）
LOBBY_POS = "7 91 6"   # /setworldspawn で指定しておくと良い
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

    # 既存ログを読み込む
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

    # 新しい進捗を追加
    prev = lines_dict.get(player_name, "")
    new_entry = f"{timestamp} {advancement_name}"
    if prev:
        new_entry = prev + " | " + new_entry
    lines_dict[player_name] = new_entry

    # 保存
    with open(adv_log_file, "w", encoding="utf-8") as f:
        for pname, advs in lines_dict.items():
            f.write(f"{pname}: {advs}\n")

# --- ボスバー更新キャッシュ ---
last_remaining = None
last_name = None

# --- ゲーム開始 ---
def start_game():
    global game_active, game_start_time, player_points, player_advancements
    global last_remaining, last_name

    last_remaining = None
    last_name = None
    start_pos = get_random_start_pos()

    # adv_output.txt をリセット
    try:
        open(adv_log_file, "w", encoding="utf-8").close()
        m_echo("adv_output.txt reset for new game")
    except Exception as e:
        m_echo(f"Failed to reset adv_output.txt: {e}")

    # スコアボードリセット
    m.execute("scoreboard objectives remove AdvPoints")
    m.execute("scoreboard objectives add AdvPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar AdvPoints")

    # 進捗リセット & アイテムクリア
    m.execute("/advancement revoke @a everything")
    m.execute("/clear @a")

    player_points = {}
    player_advancements = {}
    game_active = True
    game_start_time = time.time()

    # ボスバー設定
    m.execute('bossbar add timer "Countdown"')
    m.execute('bossbar set timer color blue')
    m.execute(f'bossbar set timer max {GAME_DURATION}')
    m.execute(f'bossbar set timer value {GAME_DURATION}')
    m.execute('bossbar set timer players @a')

    # プレイヤー移動
    m.execute(f'/spawnpoint @a {start_pos}')
    m.execute(f'/tp @a {start_pos}')

    # カウントダウン
    m.execute('/title @a title {"text":"Ready...","color":"aqua","bold":true}')
    time.sleep(1)
    for count in ["3","2","1"]:
        m.execute(f'/title @a title {{"text":"{count}","color":"aqua","bold":true}}')
        m.execute('/playsound minecraft:block.bell.use master @a')
        time.sleep(1)
    m.execute('/title @a title {"text":"Go!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.pillager.celebrate master @a')
    time.sleep(0.5)

    m_chat(f"Game Started at {start_pos}!")

# --- ゲーム終了 ---
def end_game():
    global game_active
    game_active = False

    m.execute('/title @a title {"text":"Game Over!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.pillager.celebrate master @a')

    m.execute(f"/spawnpoint @a {LOBBY_POS}")
    m.execute(f"/tp @a {LOBBY_POS}")

    sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
    colors = ["gold", "gray", "dark_aqua"]

    for i, (player, pts) in enumerate(sorted_players[:3]):
        msg = {"text": f"{i+1}位: {player} ({pts} pts)", "color": colors[i], "bold": True}
        m.execute(f'tellraw @a {json.dumps(msg)}')

    for player, pts in sorted_players[3:]:
        m_chat(f"{player}: {pts} pts")

    m.execute('bossbar remove timer')

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"adv_output_{now}.txt"
    try:
        shutil.copy(adv_log_file, backup_file)
        m_echo(f"Backup saved as {backup_file}")
    except FileNotFoundError:
        m_echo("No adv_output.txt to backup")

# --- メインループ ---
while True:
    event = eq.get()
    if event and event.type == EventType.CHAT:
        msg = event.message
        if msg.startswith("<") and ">" in msg:
            player_name, content = msg[1:].split(">", 1)
            content = content.strip()

            if content.startswith("--"):
                if game_active and not (content.startswith("--adv") or content == "--stop"):
                    m_chat("Game in progress! Only --adv and --stop are available.")
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
                        m_chat(f"Game duration set to {GAME_DURATION} seconds.")
                    else:
                        m_chat("Usage: --settime <seconds>")
                elif content == "--status":
                    m_chat(f"Game duration: {GAME_DURATION} seconds")
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
                                m.execute(f'/tell {player_name} {line.strip()}')
                                m.execute(f'/tell crocadooo {player_name} requested --adv: {line.strip()}')
                        if not found:
                            m.execute(f'/tell {player_name} No advancements found for {target}')
                            m.execute(f'/tell crocadooo {player_name} requested --adv: No advancements found for {target}')
                elif content == "--help":
                    help_texts = [
                        {"text": "\n--start : ゲーム開始", "color": "aqua", "bold": True},
                        {"text": "--stop : ゲーム終了", "color": "aqua", "bold": True},
                        {"text": "--settime <秒> : ゲーム時間設定", "color": "aqua", "bold": True},
                        {"text": "--status : 現在のゲーム時間を確認", "color": "aqua", "bold": True},
                        {"text": "--adv <プレイヤー名> : 進捗確認", "color": "aqua", "bold": True},
                        {"text": "--help : 使い方表示\n", "color": "aqua", "bold": True},
                    ]
                    for line in help_texts:
                        m.execute(f'tellraw @a {json.dumps(line)}')

    if game_active:
        elapsed = int(time.time() - game_start_time)
        remaining = max(GAME_DURATION - elapsed, 0)

        if remaining != last_remaining:
            m.execute(f'bossbar set timer value {remaining}')
            last_remaining = remaining

        mins = remaining // 60
        secs = remaining % 60
        name = f"{mins:02d}:{secs:02d}"
        if name != last_name:
            m.execute(f'bossbar set timer name "{name}"')
            last_name = name

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
            save_adv_text(player_name, advancement_name)

    time.sleep(0.05)
