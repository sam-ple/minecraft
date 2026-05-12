import minescript as m
import time
# from draw_text import draw_string

# 📦 辞書形式: particle_name → モード
particles = {
    # 🟢 通常
    "ambient_entity_effect": "normal", "angry_villager": "normal", "ash": "normal",
    "bubble": "normal", "bubble_column_up": "normal", "bubble_pop": "normal",
    "campfire_cosy_smoke": "normal", "campfire_signal_smoke": "normal", "cherry_leaves": "normal",
    "cloud": "normal", "composter": "normal", "crimson_spore": "normal", "crit": "normal",
    "current_down": "normal", "damage_indicator": "normal", "dolphin": "normal",
    "dragon_breath": "normal", "dripping_dripstone_lava": "normal", "dripping_dripstone_water": "normal",
    "dripping_honey": "normal", "dripping_lava": "normal", "dripping_obsidian_tear": "normal",
    "dripping_water": "normal", "dust_pillar": "normal", "dust_plume": "normal",
    "effect": "normal", "egg_crack": "normal", "elder_guardian": "normal",
    "electric_spark": "normal", "enchant": "normal", "enchanted_hit": "normal", "end_rod": "normal",
    "entity_effect": "normal", "explosion": "normal", "explosion_emitter": "normal",
    "falling_dripstone_lava": "normal", "falling_dripstone_water": "normal", "falling_dust": "normal",
    "falling_honey": "normal", "falling_lava": "normal", "falling_nectar": "normal",
    "falling_obsidian_tear": "normal", "falling_spore_blossom": "normal", "falling_water": "normal",
    "firefly": "normal", "firework": "normal", "fishing": "normal", "flame": "normal", "flash": "normal",
    "glow": "normal", "glow_squid_ink": "normal", "gust": "normal", "gust_emitter": "normal",
    "happy_villager": "normal", "heart": "normal", "infested": "normal", "instant_effect": "normal",
    "landing_honey": "normal", "landing_lava": "normal", "landing_obsidian_tear": "normal",
    "large_smoke": "normal", "lava": "normal", "mycelium": "normal", "nautilus": "normal", "note": "normal",
    "ominous_spawning": "normal", "pale_oak_leaves": "normal", "poof": "normal", "portal": "normal",
    "raid_omen": "normal", "rain": "normal", "reverse_portal": "normal", "scrape": "normal",
    "sculk_charge": "normal", "sculk_charge_pop": "normal", "sculk_soul": "normal", "shriek": "normal",
    "small_flame": "normal", "small_gust": "normal", "smoke": "normal", "sneeze": "normal",
    "snowflake": "normal", "sonic_boom": "normal", "soul": "normal", "soul_fire_flame": "normal",
    "spit": "normal", "splash": "normal", "spore_blossom_air": "normal", "squid_ink": "normal",
    "sweep_attack": "normal", "tinted_leaves": "normal", "totem_of_undying": "normal", "trail": "normal",
    "trial_omen": "normal", "trial_spawner_detection": "normal", "trial_spawner_detection_ominous": "normal",
    "underwater": "normal", "vault_connection": "normal", "vibration": "normal", "warped_spore": "normal",
    "wax_off": "normal", "wax_on": "normal", "white_ash": "normal", "white_smoke": "normal",
    "witch": "normal",

    # 🔶 dust系（特殊）
    "dust": "dust",
    "dust_color_transition": "dust",

    # 🔶 ブロック系
    "block_crack": "block",
    "block_dust": "block",
    "block_marker": "block",

    # 🔶 アイテム系
    "item": "item",
    "item_cobweb": "item",
    "item_slime": "item",
    "item_snowball": "item",
}

# 🖥 表示用テキスト
# text = draw_string("Preparing...", x=960, y=10, color=0xffffff, scale=4)

# 🔁 全てのパーティクルを順に処理
for i, (particle, mode) in enumerate(particles.items()):
    index = str(i + 1).zfill(2)
#    filename = f"{index}_{particle}.png"

    # パーティクルごとにコマンドを構築
    if mode == "normal":
        command = f"/particle minecraft:{particle} ~ ~1 ~ 0 0 0 0.1 20 force"

    elif mode == "block":
        command = f"/particle minecraft:{particle} minecraft:stone ~ ~1 ~ 0 0 0 0.1 20 force"

    elif mode == "item":
        item = particle.replace("item_", "minecraft:") if "_" in particle else "minecraft:apple"
        command = f"/particle minecraft:item {item} ~ ~1 ~ 0 0 0 0.1 20 force"

    elif mode == "dust":
        if particle == "dust":
            args = "1 0 0 1"
        else:  # dust_color_transition
            args = "1 0 0 1 0 0 1"
        command = f"/particle minecraft:{particle} {args} ~ ~1 ~ 0 0 0 0.1 20 force"

    else:
        m.echo(f"[!] Unknown particle mode: {mode}")
        continue

    # ✨ 表示・実行
#    m.title("", subtitle=particle)
#    text.string.set_value(command)

    time.sleep(1)
    m.execute(command)
    time.sleep(2)
#    m.screenshot(filename)
    time.sleep(1)