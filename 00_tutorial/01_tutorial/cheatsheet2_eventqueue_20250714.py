import minescript as m
import time
from queue import Empty

def title_subtitle(title, subtitle=None, delay=2):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title}","color":"gold","bold":true}}')
    if subtitle:
        m.execute(f'title @a subtitle {{"text":"{subtitle}","color":"aqua","bold":true}}')
    time.sleep(delay)

# --- KeyEvent ---
title_subtitle("KeyEvent", "Press or release any key")
with m.EventQueue() as eq:
    eq.register_key_listener()
    m.echo("-----------------------")
    m.echo("Waiting for KeyEvent... (press any key)")
    try:
        while True:
            event = eq.get(timeout=10)
            if event.type == m.EventType.KEY:
                m.echo(f"KeyEvent: key={event.key}, action={event.action}, time={event.time}")
                break
    except Empty:
        m.echo("No KeyEvent detected.")
time.sleep(2)

# --- MouseEvent ---
title_subtitle("MouseEvent", "Click any mouse button")
with m.EventQueue() as eq:
    eq.register_mouse_listener()
    m.echo("-----------------------")
    m.echo("Waiting for MouseEvent... (click mouse button)")
    try:
        while True:
            event = eq.get(timeout=10)
            if event.type == m.EventType.MOUSE:
                m.echo(f"MouseEvent: button={event.button}, action={event.action}, x={event.x}, y={event.y}")
                break
    except Empty:
        m.echo("No MouseEvent detected.")
time.sleep(2)

# --- ChatEvent ---
title_subtitle("ChatEvent", "Type a chat message and send")
with m.EventQueue() as eq:
    eq.register_chat_listener()
    m.echo("-----------------------")
    m.echo("Waiting for ChatEvent... (send chat message)")
    try:
        while True:
            event = eq.get(timeout=20)
            if event.type == m.EventType.CHAT:
                m.echo(f"ChatEvent: message='{event.message}'")
                break
    except Empty:
        m.echo("No ChatEvent detected.")
time.sleep(2)

# --- AddEntityEvent ---
title_subtitle("AddEntityEvent", "Spawn an entity nearby")
with m.EventQueue() as eq:
    eq.register_add_entity_listener()
    m.echo("-----------------------")
    m.echo("Waiting for AddEntityEvent... (spawn entity nearby)")
    try:
        while True:
            event = eq.get(timeout=20)
            if event.type == m.EventType.ADD_ENTITY:
                ent = event.entity
                uuid_str = getattr(ent, 'uuid', 'N/A')
                m.echo(f"AddEntityEvent: entity={ent.type}, UUID={uuid_str}")
                break
    except Empty:
        m.echo("No AddEntityEvent detected.")
time.sleep(2)

# --- BlockUpdateEvent ---
title_subtitle("BlockUpdateEvent", "Change a block nearby")
with m.EventQueue() as eq:
    eq.register_block_update_listener()
    m.echo("-----------------------")
    m.echo("Waiting for BlockUpdateEvent... (change a block)")
    try:
        while True:
            event = eq.get(timeout=20)
            if event.type == m.EventType.BLOCK_UPDATE:
                pos = event.position
                m.echo(f"BlockUpdateEvent: pos={pos}, old={event.old_state}, new={event.new_state}")
                break
    except Empty:
        m.echo("No BlockUpdateEvent detected.")
time.sleep(2)

# --- TakeItemEvent ---
title_subtitle("TakeItemEvent", "Pick up an item")
with m.EventQueue() as eq:
    eq.register_take_item_listener()
    m.echo("-----------------------")
    m.echo("Waiting for TakeItemEvent... (pick up item)")
    try:
        while True:
            event = eq.get(timeout=20)
            if event.type == m.EventType.TAKE_ITEM:
                item = event.item
                m.echo(f"TakeItemEvent: player_uuid={event.player_uuid}, item={getattr(item, 'type', 'N/A')}, amount={event.amount}")
                break
    except Empty:
        m.echo("No TakeItemEvent detected.")
time.sleep(2)

# --- DamageEvent ---
title_subtitle("DamageEvent", "Take damage or attack an entity")
with m.EventQueue() as eq:
    eq.register_damage_listener()
    m.echo("-----------------------")
    m.echo("Waiting for DamageEvent... (take or deal damage)")
    try:
        while True:
            event = eq.get(timeout=20)
            if event.type == m.EventType.DAMAGE:
                m.echo(f"DamageEvent: entity_uuid={event.entity_uuid}, source={event.source}")
                break
    except Empty:
        m.echo("No DamageEvent detected.")
time.sleep(2)

# --- ExplosionEvent ---
title_subtitle("ExplosionEvent", "Trigger an explosion")
with m.EventQueue() as eq:
    eq.register_explosion_listener()
    m.echo("-----------------------")
    m.echo("Waiting for ExplosionEvent... (trigger explosion)")
    try:
        while True:
            event = eq.get(timeout=20)
            if event.type == m.EventType.EXPLOSION:
                pos = event.position
                m.echo(f"ExplosionEvent: pos=({pos[0]:.1f},{pos[1]:.1f},{pos[2]:.1f})")
                break
    except Empty:
        m.echo("No ExplosionEvent detected.")
time.sleep(2)

# --- ChunkEvent ---
title_subtitle("ChunkEvent", "Load/unload chunks")
with m.EventQueue() as eq:
    eq.register_chunk_listener()
    m.echo("-----------------------")
    m.echo("Waiting for ChunkEvent... (move across chunk boundaries)")
    try:
        while True:
            event = eq.get(timeout=30)
            if event.type == m.EventType.CHUNK:
                m.echo(f"ChunkEvent: loaded={event.loaded}, area=({event.x_min},{event.z_min})-({event.x_max},{event.z_max})")
                break
    except Empty:
        m.echo("No ChunkEvent detected.")

m.echo("✅ Event listening test complete!")
