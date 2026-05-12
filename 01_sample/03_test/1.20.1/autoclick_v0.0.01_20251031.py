import minescript as m
import time

TARGET_KEYWORD = "ocelot"  # エンティティtype名に含まれるキーワード

while True:
    e = m.player_get_targeted_entity(max_distance=3)
    if e and TARGET_KEYWORD in e.type.lower():
        # m.echo(f"👀 {e.name} を見ています！")
        # 右クリック（use）
        # m.player_press_use(True)
        # m.player_press_use(False)
        # 左クリック（use）
        m.player_press_attack(True)
        m.player_press_attack(False)
        time.sleep(0.2)
    time.sleep(0.05)
