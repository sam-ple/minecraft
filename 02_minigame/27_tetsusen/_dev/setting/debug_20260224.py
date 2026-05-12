import minescript as m

# /setblock x y z minecraft:shulker_box
# /data get block x y z Items
# Get the block the player is looking at
target = m.player_get_targeted_block(max_distance=20)

if target is not None:
    # BlockPos is returned as a tuple (x, y, z)
    x, y, z = target.position
    print(f"BlockPos: x={x}, y={y}, z={z}")

    # Convert to floating point coordinates (Vector3f)
    fx, fy, fz = float(x), float(y), float(z)
    print(f"Vector3f: x={fx}, y={fy}, z={fz}")

    # Additional block info
    print(f"Block type: {target.type}")
    print(f"Face being looked at: {target.side}")
else:
    print("No block is targeted by the player.")
