from time import sleep
from datetime import datetime
import threading
import minescript as m
from minescript import (
    player_position, player_orientation, echo,
    player_get_targeted_block, player_get_targeted_entity,
    version_info, EventQueue, EventType, player_hand_items
)
from java import JavaClass
from minescript_plus import Hud, Server

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
y = 5
line_h = 15
def next_line():
    global y
    y += line_h
    return y

t_ver  = Hud.add_text("", 5, next_line())
t_pos  = Hud.add_text("", 5, next_line())
t_fps  = Hud.add_text("", 5, next_line())
t_bio  = Hud.add_text("", 5, next_line())
t_dir  = Hud.add_text("", 5, next_line())
t_time = Hud.add_text("", 5, next_line())
t_ping = Hud.add_text("", 5, next_line())
t_mob  = Hud.add_text("", 5, next_line())
t_blk  = Hud.add_text("", 5, next_line())
t_inp  = Hud.add_text("", 5, next_line())
t_hand_main = Hud.add_text("", 5, next_line())
t_hand_off  = Hud.add_text("", 5, next_line())

Hud.use_toggle_key(True)
print("MicroHUD+ started. (toggle: F12)")

# === Direction helper ===
def yaw_to_direction(yaw: float) -> str:
    # Normalize yaw to -180 ~ 180
    yaw = ((yaw + 180) % 360) - 180
    
    # Minecraft基準（0=南, +90=西, ±180=北, -90=東）
    if -22.5 <= yaw < 22.5:
        return "South"
    elif 22.5 <= yaw < 67.5:
        return "South-West"
    elif 67.5 <= yaw < 112.5:
        return "West"
    elif 112.5 <= yaw < 157.5:
        return "North-West"
    elif yaw >= 157.5 or yaw < -157.5:
        return "North"
    elif -157.5 <= yaw < -112.5:
        return "North-East"
    elif -112.5 <= yaw < -67.5:
        return "East"
    elif -67.5 <= yaw < -22.5:
        return "South-East"

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
        # === Version Info ===
        v = version_info()
        ver_text = f"VersionInfo : MC {v.minecraft} / MS {v.minescript} / {v.mod_loader} / {v.pyjinn}"

        # === Player Info ===
        x, y, z = [f"{p:.2f}" for p in player_position()]
        fps = mc.getFps()
        biome = get_biome_name()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ping = Server.get_ping()
        yaw, pitch = player_orientation()
        yaw = ((yaw + 180) % 360) - 180
        pitch = ((pitch + 180) % 360) - 180
        direction = yaw_to_direction(yaw)

        # === Entity & Block ===
        e = player_get_targeted_entity(20)
        mob_text = f"Mob: {e.type}" if e else "Mob: none"
        b = player_get_targeted_block(20)
        blk_text = f"Block: {b.type.replace('minecraft:', '')}" if b else "Block: none"

        # === Input ===
        key_names = [get_key_name(k) for k in keys_pressed]
        mouse_names = [get_mouse_name(b) for b in mouse_pressed]
        input_text = f"Keys: {', '.join(key_names) if key_names else 'None'} | Mouse: {', '.join(mouse_names) if mouse_names else 'None'}"

        # === Hands ===
        hands = m.player_hand_items()

        # main hand
        if hands.main_hand:
            main_item = hands.main_hand.get('item', 'minecraft:air') if isinstance(hands.main_hand, dict) else str(hands.main_hand)
            main_text = f"MainHand: {main_item.replace('minecraft:', '')}"
        else:
            main_text = "MainHand: empty"

        # off hand
        if hands.off_hand:
            off_item = hands.off_hand.get('item', 'minecraft:air') if isinstance(hands.off_hand, dict) else str(hands.off_hand)
            off_text = f"OffHand: {off_item.replace('minecraft:', '')}"
        else:
            off_text = "OffHand: empty"

        # === Update HUD ===
        Hud.set_text_string(t_ver,  ver_text)
        Hud.set_text_string(t_pos,  f"Pos: {x}, {y}, {z}")
        Hud.set_text_string(t_fps,  f"FPS: {fps}")
        Hud.set_text_string(t_bio,  f"Biome: {biome}")
        Hud.set_text_string(t_dir,  f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)")
        Hud.set_text_string(t_time, f"Time: {now}")
        Hud.set_text_string(t_ping, f"Ping: {ping if ping is not None else 'N/A'} ms")
        Hud.set_text_string(t_mob,  mob_text)
        Hud.set_text_string(t_blk,  blk_text)
        Hud.set_text_string(t_inp,  input_text)
        Hud.set_text_string(t_hand_main, main_text)
        Hud.set_text_string(t_hand_off,  off_text)

        sleep(0.1)

    except Exception as e:
        print(f"HUD Error: {e}")
        sleep(1)
