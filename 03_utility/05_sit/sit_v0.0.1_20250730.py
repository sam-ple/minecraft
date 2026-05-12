import minescript as m
import queue
from minescript import EventQueue, EventType
import time

SIT_TAG = "sit_stand"
is_sitting_flag = False

def sit():
    global is_sitting_flag
    if is_sitting_flag:
        m.chat("❗ You are already sitting.")
        return
    x, y, z = m.player_position()
    # Summon an invisible armor stand slightly below the player
    m.execute(f'summon minecraft:armor_stand {x:.3f} {y-2:.3f} {z:.3f} {{NoGravity:1b,Invulnerable:1b,Invisible:1b,Tags:["{SIT_TAG}"],CustomName:\'{{"text":"Sitting Stand"}}\',CustomNameVisible:0b}}')
    time.sleep(0.2)
    # Mount the player on the armor stand
    m.execute(f'ride @s mount @e[type=armor_stand,tag={SIT_TAG},sort=nearest,limit=1]')
    is_sitting_flag = True
    m.chat("🪑 You sat down.")

def stand_up():
    global is_sitting_flag
    if not is_sitting_flag:
        m.chat("❗ You are not sitting.")
        return
    # Dismount the player
    m.execute("ride @s dismount")
    # Remove the armor stand used for sitting
    m.execute(f'kill @e[type=armor_stand,tag={SIT_TAG}]')
    is_sitting_flag = False
    m.chat("🧍 You stood up.")

def toggle_sit():
    if is_sitting_flag:
        stand_up()
    else:
        sit()

def main():
    with EventQueue() as eq:
        eq.register_chat_listener()
        m.chat("✅ Type '--sit' in chat to toggle sitting or standing.")
        while True:
            try:
                event = eq.get(timeout=3)
                if event.type == EventType.CHAT:
                    msg = event.message
                    if ">" in msg:
                        msg = msg.split(">", 1)[1].strip()
                    msg = msg.lower()
                    if msg == "--sit":
                        toggle_sit()
            except queue.Empty:
                pass

if __name__ == "__main__":
    main()
