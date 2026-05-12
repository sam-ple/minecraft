"""
    @author RazrCraft
    @create date 2025-06-17 18:34:53
    @modify date 2025-11-14 15:32:56
    @desc A really simple (and perhaps buggy) scanner script that indicates at what coordinates it's discovering certain 
          blocks (configurable) in a 64 blocks radius of the player (also configurable), displaying a chat message for every 
          block (only once), and render a box in every detected block with the configured color for each type.
          Run the script to start the service, and then, to activate the scanner and display what it finds, you have to 
          press "*" key. This key bind toggle (pause/unpause) the scanner. And "-" key stops the service (terminates the 
          script). Both key binds are configurable too.
 """
import queue
from time import sleep
import types
from minescript import EventQueue, EventType, BlockPack, script_loop, render_loop, echo_json, player_position
from lib_blockpack_parser import BlockPackParser
from minescript_plus import WorldRender

### CONFIG ###

# Key binds (For other values, look here: https://www.glfw.org/docs/3.4/group__keys.html)
KEY = types.SimpleNamespace()
# KEY.TOGGLE = 332    # *
# KEY.STOP = 333      # -
KEY.TOGGLE = 61   # ^
# KEY.TOGGLE = 91   # @
KEY.STOP   = 45   # -

RADIUS = 64
SHOW_TEXT = True
RENDER_BOX = True

# Block IDs to search for
# Format: "block_id": color (r, g, b, a)
# If color is (), the white 100% alpha is used
# target_blocks = {
#     "minecraft:end_portal_frame": (126, 4, 191, 255),
#     "minecraft:infested_stone_bricks": (),
#     "minecraft:infested_cobblestone": (),
#     "minecraft:infested_mossy_stone_bricks": (),
#     "minecraft:suspicious_gravel": (),
#     "minecraft:suspicious_sand": (),
#     "minecraft:decorated_pot": (),
#     "minecraft:mud_bricks": (),
#     "minecraft:terracotta": (),
#     "minecraft:cobbled_deepslate": (),
#     "minecraft:chest": (252, 186, 3, 255),
#     "minecraft:shulker_box": (180, 59, 245, 255),
#     "minecraft:diamond_ore": (38, 219, 255, 255)
# }
# target_blocks = {
#     "minecraft:chest": (252, 186, 3, 255),
#     "minecraft:diamond_ore": (38, 219, 255, 255),
# }
target_blocks = {

    # ==================================================
    # Stronghold
    # ==================================================
    # Portal room only (max 12 blocks)
    "minecraft:end_portal_frame": (126, 4, 191, 255),

    # ==================================================
    # Ancient City
    # ==================================================
    # Unique, strong indicator (city perimeter / portal frame structure)
    "minecraft:reinforced_deepslate": (0, 255, 255, 255),

    # Medium amount inside city (not too spammy)
    "minecraft:sculk_catalyst": (0, 180, 255, 200),

    # ==================================================
    # Village
    # ==================================================
    # Usually one per village
    "minecraft:bell": (255, 255, 0, 255),

    # ==================================================
    # Nether Fortress / Dungeon
    # ==================================================
    # Blaze spawner / dungeon spawner (same ID)
    "minecraft:spawner": (255, 100, 0, 255),

    # ==================================================
    # Ocean Monument
    # ==================================================
    # Distinct underwater lighting block
    # "minecraft:sea_lantern": (0, 200, 255, 255),

    # ==================================================
    # Trial Chambers (1.21+)
    # ==================================================
    # Core block (few per structure)
    "minecraft:trial_spawner": (200, 0, 255, 255),

    # Some loot rooms contain these
    "minecraft:decorated_pot": (220, 170, 120, 180),

    # ==================================================
    # Trail Ruins
    # ==================================================
    # Archaeology indicator
    "minecraft:suspicious_gravel": (200, 150, 100, 180),

    # Desert / warm ruins archaeology
    "minecraft:suspicious_sand": (220, 200, 120, 180),

    # ==================================================
    # Iron Vein
    # ==================================================
    # Large iron vein core
    "minecraft:raw_iron_block": (255, 120, 120, 255),

    # ==================================================
    # Loot / Rare Blocks
    # ==================================================
    "minecraft:chest": (252, 186, 3, 255),
    "minecraft:shulker_box": (180, 59, 245, 255),

    # ==================================================
    # Valuable Ore
    # ==================================================
    "minecraft:diamond_ore": (38, 219, 255, 200),

    # ==================================================
    # TNT
    # ==================================================
    "minecraft:tnt": (255, 50, 50, 220),

    # ==================================================
    # Bastin
    # ==================================================
    "minecraft:lodestone": (0, 255, 180, 255), 
}
### END CONFIG ###

toggle = False
blks = set()

# set_default_executor(script_loop)
echo_json.set_required_executor(render_loop)

echo_json('[{"text":"Scanner Service started.", "color":"gold"}]')

with EventQueue() as event_queue:
    event_queue.register_key_listener()
    while True:
        try:
            if event_queue.queue.not_empty:
                event = event_queue.get(block=False)
                if event.type == EventType.KEY and event.action == 0:
                    # echo_json(f'[{{"text":"Key: {event.key}", "color":"yellow"}}]')
                    match event.key:
                        case KEY.TOGGLE:
                            toggle = not toggle
                            if toggle:
                                echo_json('[{"text":"Scanner ", "color":"white"}, {"text":"ON", "color":"green"}]')
                            else:
                                echo_json('[{"text":"Scanner ", "color":"white"}, {"text":"OFF", "color":"red"}]')
                        case KEY.STOP:
                            echo_json('[{"text":"Stopping Scanner Service...", "color":"gold"}]')
                            break
        except queue.Empty:
            pass
                
        if toggle:
            pos = player_position()
            x = round(pos[0])
            y = round(pos[1])
            z = round(pos[2])

            blockpack = BlockPack.read_world((x-RADIUS, y-RADIUS, z-RADIUS), (x+RADIUS, y+RADIUS, z+RADIUS))
            parser = BlockPackParser.parse_blockpack(blockpack)

            for tile in parser.tiles:
                for pos, block in tile.iter_setblock_params(): # type: ignore
                    blk = parser.palette[block]
                    if any(blk.startswith(b) for b in target_blocks):
                        if pos not in blks:
                            if SHOW_TEXT:
                                echo_json('[{"text":"' + blk + ' ", "color":"gray"}, {"text":"' + str(pos) + '", "color":"blue"}]')
                            if RENDER_BOX:
                                block_type = blk.split('[')[0]
                                box_color = target_blocks[block_type]
                                if box_color != ():
                                    WorldRender.add_box(*pos, *box_color)
                                else:
                                    WorldRender.add_box(*pos)
                            blks.add(pos)

        sleep(.1)
