import minescript as m
import time

"""
🎣 Auto Fishing (Endless)
- 自動キャスト、自動リール（沈み検知）
- 無限ループで釣りを続ける
- JE 1.20.1 / Minescript 4.0
"""

CHECK_INTERVAL = 0.05          # 監視間隔（秒）
SINK_THRESHOLD = -0.35         # 浮きが沈んだとみなすΔY
CAST_INTERVAL = 1.0            # 次キャストまでの待機時間（秒）


def find_newest_bobber():
    """最新の浮きエンティティを取得"""
    bobbers = [e for e in m.entities() if "fishing_bobber" in e.type.lower()]
    return max(bobbers, key=lambda e: e.id) if bobbers else None


def cast_fishing_rod():
    """釣竿を1回投げる"""
    m.player_press_use(True)
    time.sleep(0.15)
    m.player_press_use(False)
    # m.echo("🎯 釣り竿を投げました。浮きを検出中...")


def reel_fishing_rod():
    """釣竿を引く（リール）"""
    m.player_press_use(True)
    time.sleep(0.1)
    m.player_press_use(False)
    # m.echo("🎣 自動リール実行！")


def monitor_bobber(tracked_id: int):
    """浮きの動きを追跡。沈みを検出したらリール実行。"""
    last_y = None
    tick = 0

    while True:
        # 浮きの存在チェック
        bobbers = [e for e in m.entities() if "fishing_bobber" in e.type.lower()]
        bobber = next((b for b in bobbers if b.id == tracked_id), None)

        if not bobber:
            # m.echo(f"💨 浮き {tracked_id} 消失（リール後 or 魚ヒット）")
            return  # 消失で次のループへ

        y = bobber.position[1]
        if last_y is not None:
            diff = y - last_y
            tick += 1

            # 浮き沈みをログ出力
            if diff <= SINK_THRESHOLD:
                # m.echo(f"[{tick:04d}] ⬇️ 浮き沈み検知 ΔY={diff:.3f}")
                reel_fishing_rod()
                return  # 釣り上げ後、終了

        last_y = y
        time.sleep(CHECK_INTERVAL)


def main():
    # m.echo("=== 🎣 Auto Fishing (Endless Mode) ===")
    # m.echo("💡 自動キャスト＋沈み検知リール。完全自動釣りを開始します。")

    loop_count = 0
    time.sleep(1.0)

    while True:
        loop_count += 1
        # m.echo(f"\n=== 🎣 第 {loop_count} 投目 開始 ===")

        cast_fishing_rod()

        # 浮きが出現するまで待つ
        tracked_id = None
        start_time = time.time()
        while tracked_id is None and time.time() - start_time < 5:
            newest = find_newest_bobber()
            if newest:
                tracked_id = newest.id
                # m.echo(f"✅ 浮きを検出: ID={tracked_id}")
            time.sleep(0.1)

        if not tracked_id:
            # m.echo("⚠️ 浮きが見つかりません。少し待って再試行します。")
            time.sleep(2.0)
            continue

        # 浮きを監視して沈みを検知
        monitor_bobber(tracked_id)

        # 再キャスト待ち
        # m.echo(f"⏳ {CAST_INTERVAL:.1f}秒後に次のキャストを開始...")
        time.sleep(CAST_INTERVAL)


if __name__ == "__main__":
    main()
