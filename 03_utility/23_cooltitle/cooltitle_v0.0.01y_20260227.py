import minescript as m
import time

# 数字ごとの基本カラー
color_map = {
    5: "light_purple",  # ピンク
    4: "aqua",          # 水色
    3: "yellow",        # 黄色
    2: "green",         # 緑
    1: "red"            # 赤
}

def send_frame(num, white_index):
    base_color = color_map[num]
    arrows = num  # > の数

    parts = []

    # 左側
    for i in range(arrows):
        if i == white_index:
            parts.append('{"text":">","color":"white"}')
        else:
            parts.append(f'{{"text":">","color":"{base_color}"}}')

    # 数字（最後の段階だけ白）
    if white_index == arrows:
        parts.append(f'{{"text":" {num} ","color":"white"}}')
    else:
        parts.append(f'{{"text":" {num} ","color":"{base_color}"}}')

    # 右側
    for i in range(arrows):
        if i == white_index:
            parts.append('{"text":"<","color":"white"}')
        else:
            parts.append(f'{{"text":"<","color":"{base_color}"}}')

    json = '["",' + ",".join(parts) + "]"
    m.execute(f"title @a title {json}")


def countdown():
    m.execute("title @a times 0 20 0")

    for num in range(5, 0, -1):
        arrows = num

        # 白が外側 → 中央へ
        for i in range(arrows + 1):
            send_frame(num, i)
            time.sleep(1 / (arrows + 1))


countdown()

# 0演出
m.execute('title @a title {"text":"START!!","color":"white","bold":true}')
m.execute("playsound minecraft:entity.firework_rocket.launch master @a ~ ~ ~ 1 1")
