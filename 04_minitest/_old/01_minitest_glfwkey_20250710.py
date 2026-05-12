from minescript import EventQueue, EventType, echo
import time

# GLFW Key Code
GLFW_KEY_NAMES = {
    32: "SPACE",
    39: "'",
    44: ",",
    45: "-",
    46: ".",
    47: "/",
    48: "0", 49: "1", 50: "2", 51: "3", 52: "4",
    53: "5", 54: "6", 55: "7", 56: "8", 57: "9",
    59: ";", 61: "=",
    65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70: "F",
    71: "G", 72: "H", 73: "I", 74: "J", 75: "K", 76: "L", 77: "M",
    78: "N", 79: "O", 80: "P", 81: "Q", 82: "R", 83: "S", 84: "T",
    85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90: "Z",
    91: "[", 92: "\\", 93: "]", 96: "`",
    257: "ENTER",
    258: "TAB",
    259: "BACKSPACE",
    260: "INSERT",
    261: "DELETE",
    262: "RIGHT",
    263: "LEFT",
    264: "DOWN",
    265: "UP",
    266: "PAGE_UP",
    267: "PAGE_DOWN",
    268: "HOME",
    269: "END",
    280: "CAPS_LOCK",
    281: "SCROLL_LOCK",
    282: "NUM_LOCK",
    283: "PRINT_SCREEN",
    284: "PAUSE",
    290: "F1", 291: "F2", 292: "F3", 293: "F4", 294: "F5",
    295: "F6", 296: "F7", 297: "F8", 298: "F9", 299: "F10",
    300: "F11", 301: "F12",
    320: "NUMPAD_0", 321: "NUMPAD_1", 322: "NUMPAD_2", 323: "NUMPAD_3",
    324: "NUMPAD_4", 325: "NUMPAD_5", 326: "NUMPAD_6", 327: "NUMPAD_7",
    328: "NUMPAD_8", 329: "NUMPAD_9",
    330: "NUMPAD_DOT", 331: "NUMPAD_DIVIDE", 332: "NUMPAD_MULTIPLY",
    333: "NUMPAD_MINUS", 334: "NUMPAD_PLUS", 335: "NUMPAD_ENTER",
    336: "NUMPAD_EQUAL",
    340: "L_SHIFT", 341: "L_CTRL", 342: "L_ALT", 343: "L_SUPER",
    344: "R_SHIFT", 345: "R_CTRL", 346: "R_ALT", 347: "R_SUPER",
    348: "MENU",
    256: "ESCAPE",
}

def get_key_name(key_code: int) -> str:
    return GLFW_KEY_NAMES.get(key_code, f"Unknown({key_code})")

def main():
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while True:
            event = event_queue.get()
            if event.type == EventType.KEY and event.action == 0:  # when a key is released
                key_name = get_key_name(event.key)
                echo(f"{key_name} was pressed")
            time.sleep(0.01)

if __name__ == "__main__":
    main()
