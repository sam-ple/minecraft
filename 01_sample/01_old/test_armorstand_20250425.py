# # ------------------------------------------------------------
# # アーマースタンド
# # ------------------------------------------------------------
# elif user_input == "armorstand":
#     x, y, z = map(int, minescript.player_position())
#     minescript.execute(f"/tp @p {x} {y} {z} 0 0")  # 南向きに

#     # 左（東） - ネザライト装備 + トライデント
#     left_nbt = (
#         '{Invisible:0b,ShowArms:1b,ArmorItems:['
#         '  {id:"minecraft:netherite_boots",Count:1b},'
#         '  {id:"minecraft:netherite_leggings",Count:1b},'
#         '  {id:"minecraft:netherite_chestplate",Count:1b},'
#         '  {id:"minecraft:netherite_helmet",Count:1b}'
#         '],HandItems:['
#         '  {id:"minecraft:trident",Count:1b},{}]}'
#     )
#     minescript.execute(f'/summon armor_stand {x+1} {y} {z} {left_nbt}')

#     # 右（西） - ダイヤ装備 + 弓
#     # right_nbt = (
#     #     '{Invisible:0b,ShowArms:1b,ArmorItems:['
#     #     '  {id:"minecraft:diamond_boots",Count:1b},'
#     #     '  {id:"minecraft:diamond_leggings",Count:1b},'
#     #     '  {id:"minecraft:diamond_chestplate",Count:1b},'
#     #     '  {id:"minecraft:diamond_helmet",Count:1b}'
#     #     '],HandItems:['
#     #     '  {id:"minecraft:bow",Count:1b},{}]}'
#     # )
#     # 右（西） - 金装備 + クロスボウ
#     right_nbt = (
#         '{Invisible:0b,ShowArms:1b,ArmorItems:['
#         '  {id:"minecraft:golden_boots",Count:1b},'
#         '  {id:"minecraft:golden_leggings",Count:1b},'
#         '  {id:"minecraft:golden_chestplate",Count:1b},'
#         '  {id:"minecraft:golden_helmet",Count:1b}'
#         '],HandItems:['
#         '  {id:"minecraft:crossbow",Count:1b},{}]}'
#     )
#     minescript.execute(f'/summon armor_stand {x-1} {y} {z} {right_nbt}')


# elif user_input == "kill_armorstand":
#     minescript.execute('kill @e[type=minecraft:armor_stand]')
# #    minescript.execute('kill @e[type=minecraft:armor_stand,limit=1,sort=nearest]')

# ------------------------------------------------------------
# 
# ------------------------------------------------------------
elif user_input == "armorstand":
    x, y, z = map(int, minescript.player_position())
    direction = 0  # 南向き
    spacing = 1.5

    if arg1 == "reset":
        # 半径10ブロック以内のアーマースタンドをすべて削除
        minescript.execute(f"/kill @e[type=armor_stand,distance=..10]")
        minescript.echo("🗑️ アーマースタンドを全削除しました。")
        return

    # 左側3体（東方向）
    left_setups = [
        ("netherite", "trident", "shield"),
        ("iron", "sword", "totem_of_undying"),
        ("leather", "mace", "ender_pearl")
    ]

    # 右側3体（西方向）
    right_setups = [
        ("golden", "crossbow", "nautilus_shell"),
        ("diamond", "bow", "torch"),
        ("chainmail", "axe", "potion")
    ]

    def summon_stand(equip, weapon, offhand, dx):
        armor_items = ",".join([
            f'{{id:"minecraft:{equip}_boots",Count:1b}}',
            f'{{id:"minecraft:{equip}_leggings",Count:1b}}',
            f'{{id:"minecraft:{equip}_chestplate",Count:1b}}',
            f'{{id:"minecraft:{equip}_helmet",Count:1b}}'
        ])
        hand_items = f'{{id:"minecraft:{weapon}",Count:1b}},{{id:"minecraft:{offhand}",Count:1b}}'
        nbt = (
            f'{{Invisible:0b,ShowArms:1b,ArmorItems:[{armor_items}],'
            f'HandItems:[{hand_items}]}}'
        )
        minescript.execute(f"/summon armor_stand {x + dx} {y} {z} {nbt}")

    # 左側（x+）
    for i, (armor, main, off) in enumerate(left_setups):
        summon_stand(armor, main, off, spacing * (i + 1))

    # 右側（x-）
    for i, (armor, main, off) in enumerate(right_setups):
        summon_stand(armor, main, off, -spacing * (i + 1))

    minescript.echo("🛡️ アーマースタンドに装備をセットしました！")


# ------------------------------------------------------------
# 
# ------------------------------------------------------------
elif user_input == "armorstand":
    x, y, z = map(int, minescript.player_position())
    arg1 = sys.argv[2] if len(sys.argv) > 2 else None

    if arg1 == "reset":
        minescript.execute('kill @e[type=minecraft:armor_stand,tag=demo_stand]')
        minescript.echo("すべてのアーマースタンドを削除しました。")
    else:
        # プレイヤーを南向きに向けておく
        minescript.execute(f"/tp @p {x} {y} {z} 0 0")

        import random

        armor_sets = [
            ("netherite", "trident"),
            ("diamond", "bow"),
            ("golden", "crossbow"),
            ("iron", "shield"),
            ("chainmail", "sword"),
            ("leather", "fishing_rod")
        ]

        random.shuffle(armor_sets)

        for i in range(-3, 4):  # -3, -2, -1, 0, 1, 2, 3（7体）
            if i == 0:
                continue  # プレイヤー位置は除外

            ax = x + i
            armor, weapon = armor_sets[(i + 3) % len(armor_sets)]
            nbt = (
                '{Tags:["demo_stand"],Invisible:0b,ShowArms:1b,ArmorItems:['
                f'  {{id:"minecraft:{armor}_boots",Count:1b}},'
                f'  {{id:"minecraft:{armor}_leggings",Count:1b}},'
                f'  {{id:"minecraft:{armor}_chestplate",Count:1b}},'
                f'  {{id:"minecraft:{armor}_helmet",Count:1b}}'
                '],HandItems:['
                f'  {{id:"minecraft:{weapon}",Count:1b}},{{}}]}'
            )
            minescript.execute(f"/summon armor_stand {ax} {y} {z} {nbt}")

        minescript.echo("左右にアーマースタンドをランダム装備で設置しました！")