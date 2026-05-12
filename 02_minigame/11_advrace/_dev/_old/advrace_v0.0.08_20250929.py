import minescript as m
from minescript import EventQueue, EventType
import re, time
from datetime import datetime
import shutil
import random
import json

m.execute("gamerule sendCommandFeedback false")
m.execute("gamerule logAdminCommands false")

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
m.echo("Chat listener ready!")

game_active = False
game_start_time = None

# --- ログ管理 ---
adv_log_file = "adv_output.txt"

def save_adv_text(player_name, advancement_name):
    """進捗達成をプレイヤーごとに1行で時間付きで記録"""
    now = int(time.time())
    elapsed = int(now - game_start_time)  # ←ここで整数化
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

# --- （ループの外）ボスバー更新の差分キャッシュ ---
last_remaining = None
last_name = None

# --- ゲーム開始 ---
def start_game():
    global game_active, game_start_time, player_points, player_advancements, START_POS
    global last_remaining, last_name  # ここでグローバルを使ってリセット

    # 初期化（最初の1回だけ更新させる）
    last_remaining = None
    last_name = None

    # ランダムなスタート地点を選ぶ
    start_pos = get_random_start_pos()

    # --- adv_output.txt をリセット ---
    try:
        open(adv_log_file, "w", encoding="utf-8").close()
        m.echo("adv_output.txt reset for new game")
    except Exception as e:
        m.echo(f"Failed to reset adv_output.txt: {e}")

    # スコアボードリセット
    m.execute("scoreboard objectives remove AdvPoints")
    m.execute("scoreboard objectives add AdvPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar AdvPoints")

    # 進捗リセット＆アイテムクリア
    m.execute("/advancement revoke @a everything")
    m.execute("/clear @a")

    player_points = {}
    player_advancements = {}
    game_active = True
    game_start_time = time.time()

    # カウントダウンボスバー
    m.execute('bossbar add timer "Countdown"')
    m.execute('bossbar set timer color blue')
    m.execute(f'bossbar set timer max {GAME_DURATION}')
    m.execute(f'bossbar set timer value {GAME_DURATION}')
    m.execute('bossbar set timer players @a')

    # カウントダウン (3,2,1,Go!)
    m.execute('/title @a title {"text":"Ready...","color":"aqua","bold":true}')
    time.sleep(1)
    for count in ["3","2","1"]:
        m.execute(f'/title @a title {{"text":"{count}","color":"aqua","bold":true}}')
        m.execute('/playsound minecraft:block.bell.use master @a')
        time.sleep(1)
    m.execute('/title @a title {"text":"Go!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.pillager.celebrate master @a')
    time.sleep(0.5)

    # 選ばれたスタート地点に TP & spawnpoint 設定
    m.execute(f'/spawnpoint @a {start_pos}')
    m.execute(f'/tp @a {start_pos}')
    m.chat(f"Game Started at {start_pos}!")

# --- ゲーム終了 ---
def end_game():
    global game_active
    game_active = False

    # 終了タイトル・サウンド
    m.execute('/title @a title {"text":"Game Over!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.pillager.celebrate master @a')

    # 全員をロビーに戻す
    m.execute(f"/spawnpoint @a {LOBBY_POS}")
    m.execute(f"/tp @a {LOBBY_POS}")

    # 上位3位まで表示
    sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
    colors = ["gold", "gray", "dark_aqua"]  # silver → gray に変更（MC標準色）

    for i, (player, pts) in enumerate(sorted_players[:3]):
        color = colors[i]
        msg = {
            "text": f"{i+1}位: {player} ({pts} pts)",
            "color": color,
            "bold": True
        }
#        m.execute(f'tellraw @a {msg}')
        m.execute(f'tellraw @a {json.dumps(msg)}')

    # 4位以下を通常表示したい場合
    for player, pts in sorted_players[3:]:
        m.chat(f"{player}: {pts} pts")

    # ボスバー削除
    m.execute('bossbar remove timer')

    # --- ここでバックアップ ---
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"adv_output_{now}.txt"
    try:
        shutil.copy(adv_log_file, backup_file)
        m.echo(f"Backup saved as {backup_file}")
    except FileNotFoundError:
        m.echo("No adv_output.txt to backup")

# --- メインループ ---
while True:
    # 1. チャットイベント処理
    event = eq.get()
    if event and event.type == EventType.CHAT:
        msg = event.message
        if msg.startswith("<") and ">" in msg:
            player_name, content = msg[1:].split(">", 1)
            content = content.strip()

            # コマンドか通常会話か判定
            if content.startswith("--"):
                # # コマンドは crocadooo のみ許可
                # if player_name != "crocadooo":
                #     m.echo(f"{player_name} is not allowed to execute commands.")
                #     continue

                # ここで既存のコマンド処理
                if game_active and not (content.startswith("--adv") or content == "--stop"):
                    m.chat("Game in progress! Only --adv and --stop are available.")
                    continue

                if content == "--start" and not game_active:
                    start_game()
                elif content == "--stop" and game_active:
                    end_game()
                    m.chat("Game forcibly stopped.")
                elif content.startswith("--settime"):
                    parts = content.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        GAME_DURATION = int(parts[1])
                        m.chat(f"Game duration set to {GAME_DURATION} seconds.")
                    else:
                        m.chat("Usage: --settime <seconds>")
                elif content.startswith("--status"):
                    m.chat(f"Game duration: {GAME_DURATION} seconds")
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
                                # 打った本人に通知
                                m.execute(f'/tell {player_name} {line.strip()}')
                                # crocadoooにも通知
                                m.execute(f'/tell crocadooo {player_name} requested --adv: {line.strip()}')
                        if not found:
                            m.execute(f'/tell {player_name} No advancements found for {target}')
                            m.execute(f'/tell crocadooo {player_name} requested --adv: No advancements found for {target}')
                elif content.startswith("--help"):
                    help_texts = [
                        {"text": "\n--start : ゲーム開始", "color": "aqua", "bold": True},
                        {"text": "--stop : ゲーム終了", "color": "aqua", "bold": True},
                        {"text": "--settime <秒> : ゲーム時間設定", "color": "aqua", "bold": True},
                        {"text": "--status : 現在のゲーム時間を確認", "color": "aqua", "bold": True},
                        {"text": "--adv <プレイヤー名> : プレイヤーの進捗確認", "color": "aqua", "bold": True},
                        {"text": "--help : 使い方表示\n", "color": "aqua", "bold": True}
                    ]
                    for line in help_texts:
#                        m.execute(f'tellraw @a {line}')
                        m.execute(f'tellraw @a {json.dumps(line)}')

    # 2. ゲーム進行中ならタイマー更新
    if game_active:
        elapsed = int(time.time() - game_start_time)
        remaining = max(GAME_DURATION - elapsed, 0)

        # 値が変わった時だけ更新
        if remaining != last_remaining:
            m.execute(f'bossbar set timer value {remaining}')
            last_remaining = remaining

        # 名前（時間表示）が変わった時だけ更新
        mins = remaining // 60
        secs = remaining % 60
        name = f"{mins:02d}:{secs:02d}"
        if name != last_name:
            m.execute(f'bossbar set timer name "{name}"')
            last_name = name
    # 3. 進捗検知
    if game_active and event and event.type == EventType.CHAT:
        msg = event.message.strip()
        match = adv_pattern.match(msg)
        if match:
            player_name, action, advancement_name = match.groups()
            player_points[player_name] = player_points.get(player_name, 0)+1
            if player_name not in player_advancements:
                player_advancements[player_name] = []
            if advancement_name not in player_advancements[player_name]:
                player_advancements[player_name].append(advancement_name)
            # スコアボード反映
            m.execute(f"scoreboard players set {player_name} AdvPoints {player_points[player_name]}")
            m.echo(f"{player_name} earned 1 point for '{advancement_name}'! (Total: {player_points[player_name]})")
            # 進捗ログ保存
            save_adv_text(player_name, advancement_name)

    time.sleep(0.05)  # 50ms待機
