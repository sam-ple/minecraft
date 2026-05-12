import minescript as m
from minescript import EventQueue, EventType
import re, time

m.execute("gamerule sendCommandFeedback false")

# --- 初期設定 ---
GAME_DURATION = 600  # 10 minutes
START_POS = "100 64 100"  # TP座標例
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
    elapsed = now - game_start_time
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

# --- ゲーム開始 ---
def start_game():
    global game_active, game_start_time, player_points, player_advancements

    # スコアボードリセット
    m.execute("scoreboard objectives remove AdvPoints")
    m.execute("scoreboard objectives add AdvPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar AdvPoints")
    m.execute("scoreboard objectives setdisplay belowname AdvPoints")

    # 進捗リセット＆アイテムクリア
    m.execute("/advancement revoke @a everything")
    m.execute("/clear @a")

    player_points = {}
    player_advancements = {}
    game_active = True
    game_start_time = time.time()

    # カウントダウン用ボスバー
    m.execute('bossbar add timer "Countdown"')
    m.execute('bossbar set timer color blue')
    m.execute(f'bossbar set timer max {GAME_DURATION}')
    m.execute(f'bossbar set timer value {GAME_DURATION}')
    m.execute('bossbar set timer players @a')

    # タイトル・ベルで3,2,1,Go!
    m.execute('/title @a title {"text":"Ready...","color":"aqua","bold":true}')
    time.sleep(1)
    for count in ["3","2","1"]:
        m.execute(f'/title @a title {{"text":"{count}","color":"aqua","bold":true}}')
        m.execute('/playsound minecraft:block.bell.use master @a')
        time.sleep(1)
    m.execute('/title @a title {"text":"Go!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.pillager.celebrate master @a')
    time.sleep(0.5)

    # スタート地点に TP
    m.execute(f'/spawnpoint @a {START_POS}')
    m.execute(f'/tp @a {START_POS}')
    m.echo("Game Started!")

# --- ゲーム終了 ---
def end_game():
    global game_active
    game_active = False

    # 終了タイトル・サウンド
    m.execute('/title @a title {"text":"Game Over!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.pillager.celebrate master @a')

    # スタート地点に TP
    m.execute(f'/tp @a {START_POS}')

    # 結果をチャットで表示
    for player, pts in player_points.items():
        m.execute(f'say {player}: {pts} pts')
#       m.chat(f'{player}: {pts} pts')

    # # 上位3位まで表示
    # sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
    # colors = ["gold", "silver", "dark_aqua"]  # 1位:金, 2位:銀, 3位:水色

    # for i, (player, pts) in enumerate(sorted_players[:3]):
    #     color = colors[i]
    #     m.chat_json({
    #         "text": f"{i+1}位: {player} ({pts} pts)",
    #         "color": color,
    #         "bold": True
    #     })

    # # 4位以下を通常表示したい場合
    # for player, pts in sorted_players[3:]:
    #     m.chat(f"{player}: {pts} pts")

    # ボスバー削除
    m.execute('bossbar remove timer')

# --- メインループ ---
while True:
    # 1. チャットイベント処理
    event = eq.get()
    if event and event.type == EventType.CHAT:
        msg = event.message
        if msg.startswith("<") and ">" in msg:
            player_name, content = msg[1:].split(">",1)
            content = content.strip()

            # --start コマンド
            if content == "--start" and not game_active:
                start_game()

            # --adv playername コマンド
            if content.startswith("--adv"):
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
                            m.echo(line.strip())
                            found = True
                    if not found:
                        m.echo(f"No advancements found for {target}")

    # 2. ゲーム進行中ならタイマー更新
    if game_active:
        elapsed = int(time.time() - game_start_time)
        remaining = max(GAME_DURATION - elapsed, 0)
        # ボスバー更新
        m.execute(f'bossbar set timer value {remaining}')
        mins = remaining // 60
        secs = remaining % 60
        m.execute(f'bossbar set timer name "{mins:02d}:{secs:02d}"')

        if remaining <= 0:
            end_game()

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
