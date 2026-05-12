import minescript as m
from minescript import (
    player_get_targeted_entity,
    player_get_targeted_block,
    player,
    players,
    entities,
    EventQueue,
    EventType,
)
from minescript_plus import Hud
from time import sleep

hud = Hud()

# ============================================
# Configuration
# ============================================
MAX_DISTANCE = 20
TRIGGER_KEY = 344  # Right Shift (GLFW key code)

print("Press Right Shift (344) to dump FULL NBT snapshot.")

# ============================================
# Key Event Setup
# ============================================
event_queue = EventQueue()
event_queue.register_key_listener()

key_down = False  # Prevent repeat while holding key

# ============================================
# Main Loop
# ============================================
while True:
    event = event_queue.get()

    if event.type == EventType.KEY:

        # Key pressed (rising edge)
        if event.key == TRIGGER_KEY and event.action == 1 and not key_down:
            key_down = True

            lines = []
            lines.append("===== FULL NBT DEBUG SNAPSHOT =====")

            # ----------------------------------------
            # Local Player NBT
            # ----------------------------------------
            p = player(nbt=True)
            if p:
                lines.append(f"[PLAYER] {p.name}")
                lines.append(p.nbt or "No NBT")

            # ----------------------------------------
            # Targeted Entity NBT
            # ----------------------------------------
            e = player_get_targeted_entity(MAX_DISTANCE, nbt=True)
            if e:
                lines.append(f"[TARGETED ENTITY] {e.name} ({e.type})")
                lines.append(e.nbt or "No NBT")
            else:
                lines.append("[TARGETED ENTITY] None")

            # ----------------------------------------
            # Targeted Block NBT
            # ----------------------------------------
            b = player_get_targeted_block(MAX_DISTANCE)
            if b:
                x, y, z = b.position
                lines.append(f"[TARGETED BLOCK] {b.type} @ ({x},{y},{z})")

                # Fetch BlockEntity NBT via command
                m.execute('tellraw @p {"text":"---- Block NBT below(chat output below)----","color":"yellow"}')
                m.execute(f"data get block {x} {y} {z}")
            else:
                lines.append("[TARGETED BLOCK] None")

            # # ----------------------------------------
            # # Nearby Players NBT
            # # ----------------------------------------
            # near_players = players(nbt=True, max_distance=MAX_DISTANCE)
            # lines.append(f"[NEARBY PLAYERS] Count: {len(near_players)}")

            # for np in near_players:
            #     lines.append(f"- {np.name}")
            #     lines.append(np.nbt or "No NBT")

            # # ----------------------------------------
            # # Nearby Entities NBT
            # # ----------------------------------------
            # near_entities = entities(nbt=True, max_distance=MAX_DISTANCE)
            # lines.append(f"[NEARBY ENTITIES] Count: {len(near_entities)}")

            # for ne in near_entities:
            #     lines.append(f"- {ne.name} ({ne.type})")
            #     lines.append(ne.nbt or "No NBT")

            # ----------------------------------------
            # Output
            # ----------------------------------------
            output_text = "\n".join(lines)

            # Echo to chat
            m.echo(output_text)

            # Replace HUD text (limit to avoid overflow)
            # Hud.clear_all()
            # Hud.add_text(output_text[:4000], 5, 5)

        # Key released
        if event.key == TRIGGER_KEY and event.action == 0:
            key_down = False

    sleep(0.01)
