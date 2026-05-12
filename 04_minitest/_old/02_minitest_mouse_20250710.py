import minescript as m
from minescript import EventType, EventQueue
from queue import Empty

with EventQueue() as eq:
    eq.register_mouse_listener()
    m.echo("Started detecting mouse clicks")

    while True:
        try:
            event = eq.get(timeout=30)  # Raises Empty if no event occurs within 30 seconds
            if event.type == EventType.MOUSE:
                button = "Left Click" if event.button == 0 else "Right Click" if event.button == 1 else f"Button {event.button}"
                action = "pressed" if event.action == 1 else "released"
                m.echo(f"⭕️ {button} was {action}")
        except Empty:
            m.echo("❌️ No clicks for 30 seconds, continuing to wait.")
