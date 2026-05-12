import minescript as m
import time
from minescript import EventQueue, EventType

m.execute(f"give {m.player_name()} stick 1")
#m.execute(f"give {m.player_name()} stick[custom_name=\"mobcatcher\"] 1")

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

def give_spawn_egg(mob_type):
    egg = SPAWN_EGG_MAP.get(mob_type)
    if egg:
        m.execute(f"give {m.player_name()} {egg} 1")
        m.execute(f"say Spawn egg given: {egg}")
    else:
        m.execute(f"say No spawn egg mapping for mob type: {mob_type}")

def catch_mob(entity):
    mob_type = entity.type
    if not mob_type.startswith("entity.minecraft."):
        m.execute("say Invalid target — not a mob.")
        return

    m.execute(f"say Targeted mob: {mob_type}")
    give_spawn_egg(mob_type)

    try:
        m.execute(f"data merge entity {entity.uuid} {{NoAI:1b}}")
        m.execute(f"tp {entity.uuid} ~ 256 ~")
    except:
        try:
            m.execute(f"data merge entity {entity.selector} {{NoAI:1b}}")
            m.execute(f"tp {entity.selector} ~ 256 ~")
        except:
            m.execute("say Failed to teleport and freeze mob.")

def main():
    m.echo("Hold a stick and left-click a mob to catch it.")

    with EventQueue() as eq:
        eq.register_mouse_listener()

        while True:
            event = eq.get()

            # Left-click pressed (action == 1)
            if event.type == EventType.MOUSE and event.button == 0 and event.action == 1:
                hands = m.player_hand_items()
                main_hand = getattr(hands, "main_hand", None)
                if not (main_hand and getattr(main_hand, "item", "") == "minecraft:stick"):
                    continue

                target = m.player_get_targeted_entity(max_distance=3)
                if target is None:
                    m.execute("say No mob targeted.")
                    continue

                catch_mob(target)

                time.sleep(0.3)

if __name__ == "__main__":
    main()
