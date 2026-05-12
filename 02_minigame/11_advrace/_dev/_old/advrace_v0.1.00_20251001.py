import minescript as m
from minescript import EventQueue, EventType
import re, time
from datetime import datetime
import shutil
import random
import json
from queue import Empty

# Initial server setup
m.execute("gamerule sendCommandFeedback false")
# m.execute("gamerule logAdminCommands false")
m.execute("difficulty peaceful")
m.execute("time set day")
m.execute("weather clear")

# --- Helper functions ---
def m_chat(msg: str):
    """Send a green, bold message to all players"""
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": "green", "bold": True})}')

def m_echo(msg: str):
    """Send a yellow message only to the command sender"""
    m.execute(f'tellraw {m.player_name()} {json.dumps({"text": msg, "color": "yellow"})}')

# --- Game settings ---
GAME_DURATION = 600  # Game duration in seconds (10 minutes)
START_POSITIONS = [
    "-30 70 -92",
    # Add other starting positions as needed
]

def get_random_start_pos():
    """Select a random starting position from the list"""
    return random.choice(START_POSITIONS)

# Lobby position
LOBBY_POS = "7 91 6"
m.execute(f"setworldspawn {LOBBY_POS}")

player_points = {}
player_advancements = {}
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

# Setup chat listener
eq = EventQueue()
eq.register_chat_listener()
m_echo("Chat listener ready!")

game_active = False
game_start_time = None
current_start_pos = None

# Advancement log file
adv_log_file = "adv_output.txt"

def save_adv_text(player_name, advancement_name):
    """Record player's advancement with timestamp"""
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

# Boss bar update cache
last_remaining = None
last_name = None

# --- Game start function ---
def start_game():
    """Initialize game state and start the game"""
    global game_active, game_start_time, player_points, player_advancements
    global last_remaining, last_name, current_start_pos
    
    last_remaining = None
    last_name = None
    current_start_pos = get_random_start_pos()

    # Reset advancement log
    try:
        open(adv_log_file, "w", encoding="utf-8").close()
        m_echo("adv_output.txt reset for new game")
    except Exception as e:
        m_echo(f"Failed to reset adv_output.txt: {e}")

    # Setup scoreboard
    m.execute("scoreboard objectives remove AdvPoints")
    m.execute("scoreboard objectives add AdvPoints dummy Points")
    m.execute("scoreboard objectives setdisplay sidebar AdvPoints")

    # Clear player advancements and inventory
    m.execute("advancement revoke @a everything")
    m.execute("clear @a")

    player_points = {}
    player_advancements = {}
    game_active = True
    
    # Initialize boss bar
    m.execute('bossbar add timer "Countdown"')
    m.execute('bossbar set timer color blue')
    m.execute(f'bossbar set timer max {GAME_DURATION}')
    m.execute(f'bossbar set timer value {GAME_DURATION}')
    m.execute('bossbar set timer players @a')

    # Teleport all players to the starting position
    m.execute(f'spawnpoint @a {current_start_pos}')
    m.execute(f'tp @a {current_start_pos}')

    # Heal all players at game start
    m.execute("effect give @a minecraft:instant_health 1 1 true")
    m.execute("effect give @a minecraft:saturation 1 1 true")

    # Set normal difficulty and clear weather
    m.execute("difficulty normal")
    m.execute("time set day")
    m.execute("weather clear")

    # Countdown before game starts
    m.execute('title @a title {"text":"Ready...","color":"aqua","bold":true}')
    time.sleep(1)
    for count in ["3","2","1"]:
        m.execute(f'title @a title {{"text":"{count}","color":"aqua","bold":true}}')
        m.execute('playsound minecraft:block.note_block.pling master @a')
        time.sleep(1)

    game_start_time = time.time()

    # Set players to survival mode
    m.execute("gamemode survival @a")

    m.execute('title @a title {"text":"Game Start!","color":"aqua","bold":true}')
    m.execute('playsound minecraft:entity.player.levelup master @a')
    time.sleep(0.5)

    m_chat(f"Game Started at {current_start_pos}!")

# --- Game end function ---
def end_game():
    """End the game, show rankings, and return players to lobby"""
    global game_active, sorted_players
    game_active = False

    # Sort players by points
    sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
    colors = ["gold", "green", "aqua"]

    m.execute('title @a title {"text":"Game End!","color":"aqua","bold":true}')
    m.execute('playsound minecraft:entity.player.levelup master @a')

    # Set players to adventure mode
    m.execute("gamemode adventure @a")
    m.execute("difficulty peaceful")

    # Teleport players to lobby
    m.execute(f"spawnpoint @a {LOBBY_POS}")
    m.execute(f"tp @a {LOBBY_POS}")

    # Rank suffix helper
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

    # Build ranking message
    lines = [{"text": "\n"}]
    for i, (player, pts) in enumerate(sorted_players):
        rank = f"{i+1}{rank_suffix(i+1)}"
        color = colors[i] if i < len(colors) else "white"
        bold = True if i < 3 else False
        lines.append({"text": f"{rank}: {player} ({pts} pts)\n", "color": color, "bold": bold})
    lines.append({"text": "\n"})

    msg = {"text": "", "extra": lines}
    m.execute(f'tellraw @a {json.dumps(msg)}')

    m.execute('bossbar remove timer')

    # Backup advancement log
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"adv_output_{now}.txt"
    try:
        shutil.copy(adv_log_file, backup_file)
        m_echo(f"Backup saved as {backup_file}")
    except FileNotFoundError:
        m_echo("No adv_output.txt to backup")

# --- Boss bar update interval ---
last_bossbar_update = 0
BOSSBAR_INTERVAL = 1  # Update every second

# --- Main loop ---
while True:
    try:
        event = eq.get(timeout=0.05)
    except Empty:
        event = None

    if event and event.type == EventType.CHAT:
        msg = event.message
        if msg.startswith("<") and ">" in msg:
            player_name, content = msg[1:].split(">", 1)
            content = content.strip()

            if content.startswith("--"):
                # Limit available commands during an active game
                if game_active and not (content.startswith("--adv") or content in ["--stop", "--help","--status","--tp","--home"]):
                    m_chat("Game in progress! Only --adv, --help, --stop, --tp, --home are available.")
                    continue

                # Command handling
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
                        m.execute(f"tp {player_name} {current_start_pos}")
                        m_chat(f"{player_name} has joined the game area!")
                    else:
                        m_chat("No active game to join.")
                elif content == "--home":
                    m.execute(f"tp {player_name} {LOBBY_POS}")
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

        # Update boss bar value and display
        m.execute(f'bossbar set timer value {remaining}')
        mins = remaining // 60
        secs = remaining % 60
        name = f"{mins:02d}:{secs:02d}"
        m.execute(f'bossbar set timer name "{name}"')

        last_bossbar_update = current_time

        # End game when time runs out
        if remaining <= 0:
            end_game()
            m_chat("Time's up! Game ended.")

    # Track player advancements and update points
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
            m.execute('playsound minecraft:block.note_block.chime master @a')
            save_adv_text(player_name, advancement_name)
