import minescript as m
import math

R = 74
BLOCK = "minecraft:glass"

for z in range(-R, R + 1):
    max_x = int(math.sqrt(R * R - z * z))

    for x in range(-max_x, max_x + 1):
        m.execute(f"setblock ~{x} ~ ~{z} {BLOCK}")

# import minescript as m
# import math

# R = 74
# BLOCK = "minecraft:stone"

# for z in range(-R, R + 1):
#     for x in range(-R, R + 1):

#         d = x*x + z*z

#         if R*R - R <= d <= R*R + R:
#             m.execute(f"setblock ~{x} ~ ~{z} {BLOCK}")