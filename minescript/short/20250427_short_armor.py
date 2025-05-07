import time
import minescript
from minescript import (execute, echo)

def equip_set(mainhand, head, chest, legs, feet, offhand, message):
    execute(f'/item replace entity @p weapon.mainhand with {mainhand}')
    execute(f'/item replace entity @p armor.head with {head}')
    execute(f'/item replace entity @p armor.chest with {chest}')
    execute(f'/item replace entity @p armor.legs with {legs}')
    execute(f'/item replace entity @p armor.feet with {feet}')
    execute(f'/item replace entity @p weapon.offhand with {offhand}')
    
    # 装備着用音
    execute(f'/playsound minecraft:block.armor.equip_iron master @a ~ ~ ~ 1 1')  # 鉄の装備音
    echo(message)

time.sleep(5)

# 木装備（木の剣＋革防具）
equip_set(
    mainhand='minecraft:wooden_sword',
    head='minecraft:leather_helmet',
    chest='minecraft:leather_chestplate',
    legs='minecraft:leather_leggings',
    feet='minecraft:leather_boots',
    offhand='minecraft:shield',
    message='木の装備を装着しました！'
)

time.sleep(2)

# 鉄装備（鉄の剣＋鉄防具）
equip_set(
    mainhand='minecraft:iron_sword',
    head='minecraft:iron_helmet',
    chest='minecraft:iron_chestplate',
    legs='minecraft:iron_leggings',
    feet='minecraft:iron_boots',
    offhand='minecraft:ender_pearl',
    message='鉄の装備に強化しました！'
)

time.sleep(2)

# 金装備（金の剣＋金防具）
equip_set(
    mainhand='minecraft:golden_sword',
    head='minecraft:golden_helmet',
    chest='minecraft:golden_chestplate',
    legs='minecraft:golden_leggings',
    feet='minecraft:golden_boots',
    offhand='minecraft:potion',
    message='金の装備に強化しました！'
)

time.sleep(2)

# ダイヤモンド装備（ダイヤ剣＋ダイヤ防具）
equip_set(
    mainhand='minecraft:diamond_sword',
    head='minecraft:diamond_helmet',
    chest='minecraft:diamond_chestplate',
    legs='minecraft:diamond_leggings',
    feet='minecraft:diamond_boots',
    offhand='minecraft:totem_of_undying',
    message='ダイヤモンド装備を装着しました！'
)

time.sleep(2)

# ネザライト装備（メイス＋ネザライト防具）
equip_set(
    mainhand='minecraft:mace',
    head='minecraft:netherite_helmet',
    chest='minecraft:netherite_chestplate',
    legs='minecraft:netherite_leggings',
    feet='minecraft:netherite_boots',
    offhand='minecraft:trial_key',
    message='ネザライト装備（メイス装備）を装着しました！'
)

time.sleep(3)

# 2秒後にアイテムを削除
execute('/clear @p')  # プレイヤーのすべてのアイテムを削除
execute(f'/playsound minecraft:block.armor.equip_iron master @a ~ ~ ~ 1 1')  # 鉄の装備音
echo("2秒後にすべてのアイテムを削除しました！")

