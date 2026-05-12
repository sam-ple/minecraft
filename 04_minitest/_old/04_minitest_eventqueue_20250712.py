import minescript as m
import time
from queue import Empty

def title_subtitle(title, subtitle=None, delay=2):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title}","color":"gold","bold":true}}')
    if subtitle:
        m.execute(f'title @a subtitle {{"text":"{subtitle}","color":"aqua","bold":true}}')
    time.sleep(delay)

def wait_event(eq, event_type, name, instruction, timeout=30):
    m.echo("----------")
    title_subtitle(name, instruction)
    m.echo(f"[{name}] {instruction}")

    start = time.time()
    while time.time() - start < timeout:
        try:
            event = eq.get(timeout=30)
            if event.type == event_type:
                m.echo(f"⭕️ {name} received: {event}")
                time.sleep(2)
                return
        except Empty:
            pass
    m.echo(f"❌ {name} not detected.")
    time.sleep(2)

# イベントテスト実行
def main():
    m.echo("----------")
    m.echo("Starting Event Listening Test...")
    with m.EventQueue() as eq:
        eq.register_key_listener()
        eq.register_mouse_listener()
        eq.register_chat_listener()
        eq.register_add_entity_listener()
        eq.register_block_update_listener()
        eq.register_take_item_listener()
        eq.register_damage_listener()
        eq.register_explosion_listener()
        eq.register_chunk_listener()

        wait_event(eq, m.EventType.KEY,           "KeyEvent",         "Press or release any key")
        wait_event(eq, m.EventType.MOUSE,         "MouseEvent",       "Click any mouse button")
        wait_event(eq, m.EventType.CHAT,          "ChatEvent",        "Send a chat message")
        wait_event(eq, m.EventType.ADD_ENTITY,    "AddEntityEvent",   "Spawn any entity nearby")
        wait_event(eq, m.EventType.BLOCK_UPDATE,  "BlockUpdateEvent", "Change a block nearby")
        wait_event(eq, m.EventType.TAKE_ITEM,     "TakeItemEvent",    "Pick up any dropped item")
        wait_event(eq, m.EventType.DAMAGE,        "DamageEvent",      "Take or deal damage")
        wait_event(eq, m.EventType.EXPLOSION,     "ExplosionEvent",   "Trigger an explosion")
        wait_event(eq, m.EventType.CHUNK,         "ChunkEvent",       "Cross chunk boundaries")

    m.echo("----------")
    m.echo("✅ All event tests complete!")

main()
