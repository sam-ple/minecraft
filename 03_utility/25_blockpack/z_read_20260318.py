from minescript import BlockPack

bp = BlockPack.read_file("my_build")

bp.write_world(offset=(px, py, pz))

#回転コピー
bp.write_world(rotation="y90", offset=(px, py, pz))
#オフセット調整
bp.write_world(offset=(px-10, py, pz-10))
