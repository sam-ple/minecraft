from time import sleep
from datetime import datetime
from minescript import player_position, player_orientation, echo, EventQueue, EventType
from java import JavaClass
from minescript_plus import Hud, Server
import threading

# === Minecraft hooks ===
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# === GLFW Key Names ===
GLFW_KEY_NAMES = {
    32: "SPACE", 39: "'", 44: ",", 45: "-", 46: ".", 47: "/",
    48: "0", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7", 56: "8", 57: "9",
    59: ";", 61: "=", 65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70: "F",
    71: "G", 72: "H", 73: "I", 74: "J", 75: "K", 76: "L", 77: "M",
    78: "N", 79: "O", 80: "P", 81: "Q", 82: "R", 83: "S", 84: "T",
    85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90: "Z",
    91: "[", 92: "\\", 93: "]", 96: "`",
    257: "ENTER", 258: "TAB", 259: "BACKSPACE", 260: "INSERT", 261: "DELETE",
    262: "RIGHT", 263: "LEFT", 264: "DOWN", 265: "UP",
    266: "PAGE_UP", 267: "PAGE_DOWN", 268: "HOME", 269: "END",
    280: "CAPS_LOCK", 281: "SCROLL_LOCK", 282: "NUM_LOCK",
    283: "PRINT_SCREEN", 284: "PAUSE",
    290: "F1", 291: "F2", 292: "F3", 293: "F4", 294: "F5", 295: "F6",
    296: "F7", 297: "F8", 298: "F9", 299: "F10", 300: "F11", 301: "F12",
    320: "NUMPAD_0", 321: "NUMPAD_1", 322: "NUMPAD_2", 323: "NUMPAD_3",
    324: "NUMPAD_4", 325: "NUMPAD_5", 326: "NUMPAD_6", 327: "NUMPAD_7",
    328: "NUMPAD_8", 329: "NUMPAD_9",
    330: "NUMPAD_DOT", 331: "NUMPAD_DIVIDE", 332: "NUMPAD_MULTIPLY",
    333: "NUMPAD_MINUS", 334: "NUMPAD_PLUS", 335: "NUMPAD_ENTER",
    336: "NUMPAD_EQUAL",
    340: "L_SHIFT", 341: "L_CTRL", 342: "L_ALT", 343: "L_SUPER",
    344: "R_SHIFT", 345: "R_CTRL", 346: "R_ALT", 347: "R_SUPER",
    348: "MENU", 256: "ESCAPE",
}

MOUSE_NAMES = {0: "LMB", 1: "RMB", 2: "MMB"}

def get_key_name(key_code: int) -> str:
    return GLFW_KEY_NAMES.get(key_code, f"K{key_code}")

def get_mouse_name(button: int) -> str:
    return MOUSE_NAMES.get(button, f"M{button}")

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

        key_names = [get_key_name(k) for k in keys_pressed]
        mouse_names = [get_mouse_name(b) for b in mouse_pressed]
        input_text = f"Keys: {', '.join(key_names) if key_names else 'None'} | Mouse: {', '.join(mouse_names) if mouse_names else 'None'}"

        Hud.set_text_string(t_pos,  f"Pos: {x}, {y}, {z}")
        Hud.set_text_string(t_fps,  f"FPS: {fps}")
        Hud.set_text_string(t_bio,  f"Biome: {biome}")
        Hud.set_text_string(t_dir,  f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)")
        Hud.set_text_string(t_time, f"Time: {now}")
        Hud.set_text_string(t_ping, f"Ping: {ping if ping is not None else 'N/A'} ms")
        Hud.set_text_string(t_inp,  input_text)

        sleep(0.1)
    except Exception as e:
        print(f"HUD Error: {e}")
        sleep(1)
