from time import sleep
from datetime import datetime
from minescript import player_position, player_orientation, echo, EventQueue, EventType
from java import JavaClass
from minescript_plus import Hud, Server
import threading

# === Minecraft hooks ===
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# === HUD elements ===
t_pos  = Hud.add_text("Pos: ", 5, 5)
t_fps  = Hud.add_text("FPS: ", 5, 20)
t_bio  = Hud.add_text("Biome: ", 5, 35)
t_dir  = Hud.add_text("Dir: ", 5, 50)
t_time = Hud.add_text("Time: ", 5, 65)
t_ping = Hud.add_text("Ping: ", 5, 80)
t_inp  = Hud.add_text("Input: ", 5, 95)

Hud.use_toggle_key(True)
print("MicroHUD+ started. (toggle: F12)")

# === Direction helper ===
def yaw_to_direction(yaw: float) -> str:
    yaw = (yaw % 360 + 360) % 360
    if 45 <= yaw < 135:
        return "West"
    elif 135 <= yaw < 225:
        return "North"
    elif 225 <= yaw < 315:
        return "East"
    else:
        return "South"

# === Biome getter ===
def get_biome_name():
    if mc.level is None or mc.player is None:
        return "Unknown"
    try:
        player_pos = mc.player.blockPosition()
        biome_holder = mc.level.getBiome(player_pos)
        biome_key = biome_holder.unwrapKey().get()
        return biome_key.location().toString().replace("minecraft:", "")
    except Exception:
        return "Unknown"

# === Input tracking ===
key_map = {340:"LShift", 341:"RShift", 32:"Space", 65:"A",68:"D",87:"W",83:"S"}
mouse_map = {0:"LMB",1:"RMB",2:"MMB"}

keys_pressed = set()
mouse_pressed = set()

eq = EventQueue()
eq.register_key_listener()
eq.register_mouse_listener()

def process_input_events():
    while True:
        e = eq.get()
        if e.type == EventType.KEY:
            if e.action == 1:
                keys_pressed.add(e.key)
            elif e.action == 0:
                keys_pressed.discard(e.key)
        elif e.type == EventType.MOUSE:
            if e.action == 1:
                mouse_pressed.add(e.button)
            elif e.action == 0:
                mouse_pressed.discard(e.button)
        sleep(0.01)

threading.Thread(target=process_input_events, daemon=True).start()

# === Main loop ===
while True:
    try:
        x, y, z = [f"{p:.2f}" for p in player_position()]
        fps = mc.getFps()
        biome = get_biome_name()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ping = Server.get_ping()
        yaw, pitch = player_orientation()
        direction = yaw_to_direction(yaw)

        # 入力文字列
        key_names = [key_map.get(k, f"K{k}") for k in keys_pressed]
        mouse_names = [mouse_map.get(b, f"B{b}") for b in mouse_pressed]
        input_text = f"Keys: {', '.join(key_names) if key_names else 'None'} | Mouse: {', '.join(mouse_names) if mouse_names else 'None'}"

        Hud.set_text_string(t_pos,  f"Pos: {x}, {y}, {z}")
        Hud.set_text_string(t_fps,  f"FPS: {fps}")
        Hud.set_text_string(t_bio,  f"Biome: {biome}")
        Hud.set_text_string(t_dir,  f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)")
        Hud.set_text_string(t_time, f"Time: {now}")
        Hud.set_text_string(t_ping, f"Ping: {ping if ping is not None else 'N/A'} ms")
        Hud.set_text_string(t_inp,  input_text)

        sleep(0.5)
    except Exception as e:
        print(f"HUD Error: {e}")
        sleep(1)
