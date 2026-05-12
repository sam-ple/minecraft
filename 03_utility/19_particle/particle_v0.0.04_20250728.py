import minescript as m
import time
# from draw_text import draw_string

# List of all particle types
particles = [
    "ambient_entity_effect", "angry_villager", "ash", "block_crack",
    "block_dust", "block_marker", "bubble", "bubble_column_up",
    "bubble_pop", "campfire_cosy_smoke", "campfire_signal_smoke",
    "cherry_leaves", "cloud", "composter", "crimson_spore",
    "crit", "current_down", "damage_indicator", "dolphin",
    "dragon_breath", "dripping_dripstone_lava", "dripping_dripstone_water",
    "dripping_honey", "dripping_lava", "dripping_obsidian_tear",
    "dripping_water", "dust", "dust_color_transition", "dust_pillar",
    "dust_plume", "effect", "egg_crack", "elder_guardian",
    "electric_spark", "enchant", "enchanted_hit", "end_rod",
    "entity_effect", "explosion", "explosion_emitter",
    "falling_dripstone_lava", "falling_dripstone_water", "falling_dust",
    "falling_honey", "falling_lava", "falling_nectar",
    "falling_obsidian_tear", "falling_spore_blossom", "falling_water",
    "firefly", "firework", "fishing", "flame", "flash",
    "glow", "glow_squid_ink", "gust", "gust_emitter",
    "happy_villager", "heart", "infested", "instant_effect",
    "item", "item_cobweb", "item_slime", "item_snowball",
    "landing_honey", "landing_lava", "landing_obsidian_tear",
    "large_smoke", "lava", "mycelium", "nautilus", "note",
    "ominous_spawning", "pale_oak_leaves", "poof", "portal",
    "raid_omen", "rain", "reverse_portal", "scrape",
    "sculk_charge", "sculk_charge_pop", "sculk_soul", "shriek",
    "small_flame", "small_gust", "smoke", "sneeze",
    "snowflake", "sonic_boom", "soul", "soul_fire_flame",
    "spit", "splash", "spore_blossom_air", "squid_ink",
    "sweep_attack", "tinted_leaves", "totem_of_undying", "trail",
    "trial_omen", "trial_spawner_detection", "trial_spawner_detection_ominous",
    "underwater", "vault_connection", "vibration", "warped_spore",
    "wax_off", "wax_on", "white_ash", "white_smoke",
    "witch"
]

# Display text
# text = draw_string("Preparing...", x=960, y=10, color=0xffffff, scale=4)
# text = draw_centered_string("Preparing...", y=10, color=0xffffff, scale=4)

for i, particle in enumerate(particles):
    index = str(i + 1).zfill(2)
    filename = f"{index}_{particle}.png"
    command = f"/particle minecraft:{particle} ~ ~1 ~"

    # Show particle name in subtitle and update draw_text
    m.execute(f"title {m.player_name()} subtitle {{\"text\":\"{particle}\",\"color\":\"white\"}}")
    # text.string.set_value(f"{command}")

    # Execute the particle command after 1 second
    time.sleep(1)
    m.execute(command)

    # Take a screenshot 2 seconds after execution
    time.sleep(2)
#    m.screenshot(filename)

    # Wait 1 more second before moving to the next particle (total 4 seconds per particle)
    time.sleep(1)
