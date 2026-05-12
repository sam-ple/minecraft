import minescript as m
import time

# スコアボード作成（ゾンビ討伐用）
m.execute("scoreboard objectives add zombie_kill minecraft.killed:minecraft.zombie")
m.execute("scoreboard objectives setdisplay sidebar zombie_kill")