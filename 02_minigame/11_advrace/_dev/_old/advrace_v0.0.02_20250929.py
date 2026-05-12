import minescript as m
from minescript import EventQueue, EventType
import re, time

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

def start_game():
    global game_active, game_start_time, player_points, player_advancements

    # スコアボードリセット
    m.execute("scoreboard objectives remove AdvPoints")
    m.execute("scoreboard objectives add AdvPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar AdvPoints")

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

def end_game():
    global game_active

    game_active = False

    # 終了タイトル・サウンド
    m.execute('/title @a title {"text":"Game Over!","color":"aqua","bold":true}')
    m.execute('/playsound minecraft:entity.pillager.celebrate master @a')

    # プレイヤーをスタート地点に TP
    m.execute(f'/tp @a {START_POS}')

    # 結果をチャットで表示
    for player, pts in player_points.items():
        m.execute(f'say {player}: {pts} pts')

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
