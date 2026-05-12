# init.py
# ──────────────────────────────
# Minecraft サーバー 初期化スクリプト（Python + m.execute）
# すべての主要コマンドをカテゴリ別に統合
# 必要に応じてコメントアウトで有効/無効を切替
# ──────────────────────────────

import minescript as m

# ────── サーバー基本設定 ──────
# コマンドフィードバックを非表示
m.execute("gamerule sendCommandFeedback false")

# 自動時間進行の停止（時間固定用）
# m.execute("gamerule doDaylightCycle false")
# 昼に設定
# m.execute("time set day")

# Mob の自然スポーン制御
# m.execute("gamerule doMobSpawning false")  # モブを湧かせない
# m.execute("gamerule doMobLoot true")       # モブのドロップ有効

# 火災や草の燃焼を防ぐ
# m.execute("gamerule doFireTick false")

# ────── 天候・環境操作 ──────
# m.execute("weather clear")
# m.execute("weather rain 1000")
# m.execute("weather thunder 2000")
# m.execute("difficulty normal")

# ブロック・環境操作
# m.execute("setblock 0 64 0 minecraft:stone")
# m.execute("fill 0 64 0 10 70 10 minecraft:glass replace")
# m.execute("clone 0 64 0 10 70 10 20 64 20")

# ────── プレイヤー管理 ──────
# ゲームモード設定
# m.execute("gamemode survival @a")
# m.execute("gamemode creative @a")
# m.execute("gamemode adventure @a")

# スポーン地点
# m.execute("setworldspawn 0 64 0")
# m.execute("spawnpoint @a 0 64 0")

# XP/ステータス
# m.execute("effect clear @a")
# m.execute("xp set @a 0 levels")

# プレイヤー操作
# m.execute("ban <player>")
# m.execute("pardon <player>")
# m.execute("op <player>")
# m.execute("deop <player>")
# m.execute("kick @a メンテナンス中です")

# サーバー管理 / プレイヤー管理
# /op <player> … プレイヤーを管理者にする
# /deop <player> … 管理者権限を外す
# /whitelist add <player> … ホワイトリストに追加
# /whitelist remove <player> … ホワイトリストから削除
# /whitelist list … 登録されているプレイヤー一覧
# /whitelist on … ホワイトリスト有効化
# /whitelist off … 無効化
# /kick <player> … プレイヤーをキック
# /ban <player> … BAN
# /pardon <player> … BAN解除

# ────── アイテム配布 ──────
# 基本武器・道具
# m.execute("give @a minecraft:nether_sword 1")
# m.execute("give @a minecraft:diamond_pickaxe{Enchantments:[{id:efficiency,lvl:5}]} 1")

# ポーション・特殊アイテム
# m.execute("give @a minecraft:potion{Potion:\"minecraft:strong_healing\"} 1")
# m.execute("give @a minecraft:enchanted_golden_apple 1")

# ────── エフェクト・ステータス ──────
# m.execute("effect give @a minecraft:strength 60 1")
# m.execute("effect give @a minecraft:speed 300 1")
# m.execute("effect give @a minecraft:resistance 600 0")
# m.execute("effect clear @a")

# ────── 条件付き・高度コマンド ──────
# 条件付き実行例
# m.execute("execute as @a if entity @s[distance=..10] run say 近くにいる！")

# エンティティ操作
# m.execute("summon minecraft:zombie 0 64 0")
# m.execute("kill @e[type=minecraft:zombie]")

# エンティティデータ操作
# m.execute("data get entity @a Health")
# m.execute("data merge entity @a {CustomName:'\"Hero\"'}")
# m.execute("data remove entity @a Health")

# ────── タイトル・サウンド・パーティクル ──────
# タイトル表示
# m.execute('title @a title {"text":"Welcome!"}')
# m.execute('title @a subtitle {"text":"準備はいいですか？"}')

# サウンド再生
# m.execute("playsound minecraft:entity.player.levelup master @a")
# パーティクル生成
# m.execute("particle minecraft:flame ~ ~1 ~ 0 0 0 0 10 force @a")

# ────── スコアボード・アドバンスメント ──────
# m.execute("scoreboard objectives add kills dummy 'Kill Count'")
# m.execute("scoreboard players set @a kills 0")
# m.execute("advancement grant @a everything")

# ────── 関数・戦利品 ──────
# m.execute("function my_namespace:spawn_items")
# m.execute("loot give @a loot minecraft:chests/simple_dungeon")

# ────── コメントアウトの使い方 ──────
# 実行したくないコマンドは先頭に # を付ける
# 必要に応じてコメント解除するだけで有効化可能

# ────── 最後にサーバー全体保存（オプション） ──────
# m.execute("save-all")
