# ============================================================
# Chat Log System
# Version : v0.1.00
# Date: 2026-03-05
#
# Minecraft Java Edition + MineScript
#
# File
#   chatlog.py
#
# Features
#   ・Minecraftチャットをリアルタイム監視
#   ・すべてのチャットメッセージをログ保存
#   ・タイムスタンプ付きテキストログ
#
# Output
#   minescript/data/chatlog/chatlog.txt
#
# Notes
#   ・MineScript EventQueue を使用
#   ・チャットイベントのみを処理
# ============================================================

import minescript as m
from minescript import EventQueue, EventType
import datetime
import os


# ============================================================
# DATA DIRECTORY
# ログ保存先ディレクトリ
# ============================================================

BASE_DIR = "minescript/data/chatlog"

# ディレクトリが存在しない場合は作成
os.makedirs(BASE_DIR, exist_ok=True)

# ログファイルパス
LOG_FILE = f"{BASE_DIR}/chatlog.txt"


# ============================================================
# LOG FUNCTION
# チャットメッセージをファイルへ追記する
# ============================================================

def log_message(msg: str):
    """
    チャットメッセージをログファイルへ保存

    Parameters
    ----------
    msg : str
        Minecraftチャットメッセージ
    """

    # 現在時刻取得
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ログファイルへ追記
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")


# ============================================================
# EVENT LISTENER INITIALIZATION
# MineScriptのイベントキューを準備
# ============================================================

eq = EventQueue()

# チャットイベントを監視対象に登録
eq.register_chat_listener()

# 起動メッセージ
m.echo("Chat listener ready! Logging ALL chat messages...")


# ============================================================
# MAIN LOOP
# チャットイベントを待機しログ保存
# ============================================================

while True:

    # イベント取得（ブロッキング）
    event = eq.get()

    # チャット以外のイベントは無視
    if not event or event.type != EventType.CHAT:
        continue

    # チャットメッセージ取得
    msg = event.message

    # ログ保存
    log_message(msg)