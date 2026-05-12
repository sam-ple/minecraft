from minescript import EventQueue, EventType, show_chat_screen

# GLFW key code: Right Shift
key_code = 344

# List of messages to cycle through (add as many as you like)
messages = [
    '\\eval "echo(\\"Hello World!\\")"',
    '-------------',
    '\\eval "import time" "echo(\\"Good Morning\\")" "time.sleep(3)"  "echo(\\"Good Afternoon\\")" ',
    '-------------',
    '\\eval "echo_json({\\"text\\": \\"This is red text\\", \\"color\\": \\"red\\"})"',
    '-------------',
    '\\eval "player_press_forward(True)"',
    '\\eval "player_press_forward(False)"',
    '\\eval "player_press_backward(True)"',
    '\\eval "player_press_backward(False)"',
    '\\eval "player_press_left(True)"',
    '\\eval "player_press_left(False)"',
    '\\eval "player_press_jump(True)"',
    '\\eval "player_press_jump(False)"',
    '\\eval "player_press_sneak(True)"',
    '\\eval "player_press_sneak(False)"',
    '\\eval "player_press_swap_hands(True)"',
    '\\eval "player_press_swap_hands(True)"',
    '-------------',
    '\\eval "version_info()"',
    '-------------',
    '\\eval "world_info()"',
    '-------------',
    '\\eval "player_name()"',
    '-------------',
    '\\eval "player_position()"',
    '-------------',
    '\\eval "player_orientation()"',
    '-------------',
    '\\eval "player_hand_items()"',
    '-------------',
    '\\eval "player_inventory()"',
    '-------------',
    '\\eval "player_health()"',
    '-------------',
    '\\eval "players(limit=2)"',
    '-------------',
    '\\eval "entities(limit=2)"',
    '-------------',
    '\\eval "entities(limit=2,name=\\"Pig\\")"',
    '-------------',
]

# Current index in the message list
index = 0

with EventQueue() as event_queue:
    event_queue.register_key_listener()
    while True:
        event = event_queue.get()
        if event.type == EventType.KEY and event.action == 0 and event.key == key_code:
            # Get the message to display in the chat input
            message = messages[index]
            show_chat_screen(True, message)

            # Move to the next index (loop back to 0 if at the end)
            index = (index + 1) % len(messages)
