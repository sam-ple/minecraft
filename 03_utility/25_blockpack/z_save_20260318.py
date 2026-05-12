from minescript import BlockPack

bp = BlockPack.read_world((x1, y1, z1), (x2, y2, z2))

bp.write_file("my_build")

# # コメント付き保存
# bp = BlockPack.read_world(
#     (x1,y1,z1), (x2,y2,z2),
#     comments={"name": "castle", "author": "me"}
# )

# # base64化（通信・共有用
# data = bp.export_data()