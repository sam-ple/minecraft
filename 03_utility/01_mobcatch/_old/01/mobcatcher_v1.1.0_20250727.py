import minescript as m
import time
from minescript import EventQueue, EventType

# 初期設定
DEFAULTS = {
    "catch_item": "minecraft:stick",
    "hand_type": "onhand",
    "click_type": "left",
    "max_dist": 3
}
catch_item = DEFAULTS["catch_item"]
hand_type = DEFAULTS["hand_type"]
click_type = DEFAULTS["click_type"]
max_dist = DEFAULTS["max_dist"]

SPAWN_EGG_MAP = {
    "entity.minecraft.allay":           "minecraft:allay_spawn_egg",
    "entity.minecraft.armadillo":      "minecraft:armadillo_spawn_egg",
    "entity.minecraft.axolotl":        "minecraft:axolotl_spawn_egg",
    "entity.minecraft.bat":            "minecraft:bat_spawn_egg",
    "entity.minecraft.bee":            "minecraft:bee_spawn_egg",
    "entity.minecraft.blaze":          "minecraft:blaze_spawn_egg",
    "entity.minecraft.bogged":         "minecraft:bogged_spawn_egg",
    "entity.minecraft.breeze":         "minecraft:breeze_spawn_egg",
    "entity.minecraft.camel":          "minecraft:camel_spawn_egg",
    "entity.minecraft.cat":            "minecraft:cat_spawn_egg",
    "entity.minecraft.cave_spider":    "minecraft:cave_spider_spawn_egg",
    "entity.minecraft.chicken":        "minecraft:chicken_spawn_egg",
    "entity.minecraft.cod":            "minecraft:cod_spawn_egg",
    "entity.minecraft.cow":            "minecraft:cow_spawn_egg",
    "entity.minecraft.creaking":       "minecraft:creaking_spawn_egg",
    "entity.minecraft.creeper":        "minecraft:creeper_spawn_egg",
    "entity.minecraft.dolphin":        "minecraft:dolphin_spawn_egg",
    "entity.minecraft.donkey":         "minecraft:donkey_spawn_egg",
    "entity.minecraft.drowned":        "minecraft:drowned_spawn_egg",
    "entity.minecraft.elder_guardian": "minecraft:elder_guardian_spawn_egg",
    "entity.minecraft.ender_dragon":   "minecraft:ender_dragon_spawn_egg",
    "entity.minecraft.enderman":       "minecraft:enderman_spawn_egg",
    "entity.minecraft.endermite":      "minecraft:endermite_spawn_egg",
    "entity.minecraft.evoker":         "minecraft:evoker_spawn_egg",
    "entity.minecraft.fox":            "minecraft:fox_spawn_egg",
    "entity.minecraft.frog":           "minecraft:frog_spawn_egg",
    "entity.minecraft.ghast":          "minecraft:ghast_spawn_egg",
    "entity.minecraft.glow_squid":     "minecraft:glow_squid_spawn_egg",
    "entity.minecraft.goat":           "minecraft:goat_spawn_egg",
    "entity.minecraft.guardian":       "minecraft:guardian_spawn_egg",
    "entity.minecraft.hoglin":         "minecraft:hoglin_spawn_egg",
    "entity.minecraft.horse":          "minecraft:horse_spawn_egg",
    "entity.minecraft.husk":           "minecraft:husk_spawn_egg",
    "entity.minecraft.iron_golem":     "minecraft:iron_golem_spawn_egg",
    "entity.minecraft.llama":          "minecraft:llama_spawn_egg",
    "entity.minecraft.magma_cube":     "minecraft:magma_cube_spawn_egg",
    "entity.minecraft.mooshroom":      "minecraft:mooshroom_spawn_egg",
    "entity.minecraft.mule":           "minecraft:mule_spawn_egg",
    "entity.minecraft.ocelot":         "minecraft:ocelot_spawn_egg",
    "entity.minecraft.panda":          "minecraft:panda_spawn_egg",
    "entity.minecraft.parrot":         "minecraft:parrot_spawn_egg",
    "entity.minecraft.phantom":        "minecraft:phantom_spawn_egg",
    "entity.minecraft.pig":            "minecraft:pig_spawn_egg",
    "entity.minecraft.piglin":         "minecraft:piglin_spawn_egg",
    "entity.minecraft.piglin_brute":   "minecraft:piglin_brute_spawn_egg",
    "entity.minecraft.pillager":       "minecraft:pillager_spawn_egg",
    "entity.minecraft.polar_bear":     "minecraft:polar_bear_spawn_egg",
    "entity.minecraft.pufferfish":     "minecraft:pufferfish_spawn_egg",
    "entity.minecraft.rabbit":         "minecraft:rabbit_spawn_egg",
    "entity.minecraft.ravager":        "minecraft:ravager_spawn_egg",
    "entity.minecraft.salmon":         "minecraft:salmon_spawn_egg",
    "entity.minecraft.sheep":          "minecraft:sheep_spawn_egg",
    "entity.minecraft.shulker":        "minecraft:shulker_spawn_egg",
    "entity.minecraft.silverfish":     "minecraft:silverfish_spawn_egg",
    "entity.minecraft.skeleton":       "minecraft:skeleton_spawn_egg",
    "entity.minecraft.skeleton_horse": "minecraft:skeleton_horse_spawn_egg",
    "entity.minecraft.slime":          "minecraft:slime_spawn_egg",
    "entity.minecraft.sniffer":        "minecraft:sniffer_spawn_egg",
    "entity.minecraft.snow_golem":     "minecraft:snow_golem_spawn_egg",
    "entity.minecraft.squid":          "minecraft:squid_spawn_egg",
    "entity.minecraft.stray":          "minecraft:stray_spawn_egg",
    "entity.minecraft.strider":        "minecraft:strider_spawn_egg",
    "entity.minecraft.tadpole":        "minecraft:tadpole_spawn_egg",
    "entity.minecraft.trader_llama":   "minecraft:trader_llama_spawn_egg",
    "entity.minecraft.tropical_fish":  "minecraft:tropical_fish_spawn_egg",
    "entity.minecraft.turtle":         "minecraft:turtle_spawn_egg",
    "entity.minecraft.vex":            "minecraft:vex_spawn_egg",
    "entity.minecraft.vindicator":    "minecraft:vindicator_spawn_egg",
    "entity.minecraft.villager":      "minecraft:villager_spawn_egg",
    "entity.minecraft.wandering_trader":"minecraft:wandering_trader_spawn_egg",
    "entity.minecraft.warden":         "minecraft:warden_spawn_egg",
    "entity.minecraft.witch":          "minecraft:witch_spawn_egg",
    "entity.minecraft.wither":"minecraft:wither_spawn_egg",
    "entity.minecraft.wither_skeleton":"minecraft:wither_skeleton_spawn_egg",
    "entity.minecraft.wolf":           "minecraft:wolf_spawn_egg",
    "entity.minecraft.zoglin":          "minecraft:zoglin_spawn_egg",
    "entity.minecraft.zombie":         "minecraft:zombie_spawn_egg",
    "entity.minecraft.zombie_horse":   "minecraft:zombie_horse_spawn_egg",
    "entity.minecraft.zombified_piglin":"minecraft:zombified_piglin_spawn_egg",
    "entity.minecraft.zombie_villager":"minecraft:zombie_villager_spawn_egg",
}

def tell(msg, color="white"):
    m.execute(f'tellraw {m.player_name()} {{"text":"{msg}","color":"{color}"}}')

def tell_multiline(lines):
    text = ",".join(f'{{"text":"{line}\\n"}}' for line in lines)
    m.execute(f'tellraw {m.player_name()} [{text}]')

def give_spawn_egg(mob_type):
    egg = SPAWN_EGG_MAP.get(mob_type)
    if egg:
        m.execute(f"give {m.player_name()} {egg} 1")
        tell(f"🥚 Spawn egg given: {egg}", "green")
    else:
        tell(f"❌ No spawn egg mapping for mob type: {mob_type}", "red")

def catch_mob(entity):
    mob_type = entity.type
    if not mob_type.startswith("entity.minecraft."):
        tell("❌ Invalid target — not a mob.", "red")
        return

    tell(f"🎯 Targeted mob: {mob_type}", "yellow")
    give_spawn_egg(mob_type)

    try:
        m.execute(f"data merge entity {entity.uuid} {{NoAI:1b}}")
        m.execute(f"tp {entity.uuid} ~ 256 ~")
    except:
        try:
            m.execute(f"data merge entity {entity.selector} {{NoAI:1b}}")
            m.execute(f"tp {entity.selector} ~ 256 ~")
        except:
            tell("⚠️ Failed to teleport and freeze mob.", "red")

def process_command(msg):
    global catch_item, hand_type, click_type, max_dist

    if msg.startswith("<") and ">" in msg:
        msg = msg.split(">", 1)[1].strip()

    args = msg.strip().split()
    if not args:
        return

    cmd = args[0]
    if cmd == "--setitem" and len(args) == 2:
        catch_item = args[1]
        m.execute(f"give {m.player_name()} {catch_item} 1")
        tell(f"🎁 Catch item set to {catch_item} and given.", "green")
    elif cmd == "--sethand" and len(args) == 2:
        if args[1] in ("onhand", "offhand"):
            hand_type = args[1]
            tell(f"✋ Hand set to {hand_type}.", "green")
        else:
            tell("❌ Invalid hand. Use onhand/offhand.", "red")
    elif cmd == "--setclick" and len(args) == 2:
        if args[1] in ("left", "right"):
            click_type = args[1]
            tell(f"🖱️ Click set to {click_type}.", "green")
        else:
            tell("❌ Invalid click. Use left/right.", "red")
    elif cmd == "--setdist" and len(args) == 2:
        try:
            dist = float(args[1])
            if dist > 0:
                max_dist = dist
                tell(f"📏 Distance set to {max_dist}.", "green")
            else:
                tell("❌ Distance must be positive.", "red")
        except:
            tell("❌ Invalid distance value.", "red")
    elif cmd == "--info":
        tell_multiline([
            "ℹ️ Current settings:",
            f"• Catch item: {catch_item}",
            f"• Hand: {hand_type}",
            f"• Click: {click_type}",
            f"• Max distance: {max_dist}"
        ])
    elif cmd == "--reset":
        catch_item = DEFAULTS["catch_item"]
        hand_type = DEFAULTS["hand_type"]
        click_type = DEFAULTS["click_type"]
        max_dist = DEFAULTS["max_dist"]
        tell_multiline([
            "♻️ Settings reset to default:",
            f"• Catch item: {catch_item}",
            f"• Hand: {hand_type}",
            f"• Click: {click_type}",
            f"• Max distance: {max_dist}"
        ])
    elif cmd == "--help":
        tell_multiline([
            "🔧 Available Commands:",
            "• --setitem <item>",
            "• --sethand onhand/offhand",
            "• --setclick left/right",
            "• --setdist <number>",
            "• --info",
            "• --reset",
            "• --help"
        ])
    # else:
    #     tell("❓ Unknown command. Use --help for list.", "yellow")

def is_click_match(event):
    if click_type == "left":
        return event.button == 0 and event.action == 1
    else:
        return event.button == 1 and event.action == 1

def get_player_item_in_hand():
    hands = m.player_hand_items()
    return getattr(hands, "main_hand", None) if hand_type == "onhand" else getattr(hands, "off_hand", None)

def main():
    tell("🎯 Hold the catch item and click a mob to catch it. Use --help for commands.", "aqua")

    with EventQueue() as eq:
        eq.register_mouse_listener()
        eq.register_chat_listener()

        while True:
            event = eq.get()

            if event.type == EventType.CHAT:
                process_command(event.message)
                continue

            if event.type == EventType.MOUSE:
                if is_click_match(event):
                    item = get_player_item_in_hand()
                    if not (item and getattr(item, "item", "") == catch_item):
                        continue

                    target = m.player_get_targeted_entity(max_distance=max_dist)
                    if target is None:
                        tell("📭 No mob targeted.", "gray")
                        continue

                    catch_mob(target)
                    time.sleep(0.3)

if __name__ == "__main__":
    main()
