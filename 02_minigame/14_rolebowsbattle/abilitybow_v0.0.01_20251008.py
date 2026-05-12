import minescript as m

# 各種「効果付きの矢」リスト
arrows = [
    {"name": "暗視の矢", "potion": "night_vision", "count": 5},
    {"name": "暗視の矢-延長", "potion": "long_night_vision", "count": 5},
    {"name": "透明化の矢", "potion": "invisibility", "count": 5},
    {"name": "透明化の矢-延長", "potion": "long_invisibility", "count": 5},
    {"name": "跳躍の矢", "potion": "leaping", "count": 5},
    {"name": "跳躍の矢-延長", "potion": "long_leaping", "count": 5},
    {"name": "跳躍の矢-強化", "potion": "strong_leaping", "count": 5},
    {"name": "耐火の矢", "potion": "fire_resistance", "count": 5},
    {"name": "耐火の矢-延長", "potion": "long_fire_resistance", "count": 5},
    {"name": "俊敏の矢", "potion": "swiftness", "count": 5},
    {"name": "俊敏の矢-延長", "potion": "long_swiftness", "count": 5},
    {"name": "俊敏の矢-強化", "potion": "strong_swiftness", "count": 5},
    {"name": "鈍化の矢", "potion": "slowness", "count": 5},
    {"name": "鈍化の矢-延長", "potion": "long_slowness", "count": 5},
    {"name": "鈍化の矢-強化", "potion": "strong_slowness", "count": 5},
    {"name": "タートルマスターの矢", "potion": "turtle_master", "count": 5},
    {"name": "タートルマスターの矢-延長", "potion": "long_turtle_master", "count": 5},
    {"name": "タートルマスターの矢-強化", "potion": "strong_turtle_master", "count": 5},
    {"name": "水中呼吸の矢", "potion": "water_breathing", "count": 5},
    {"name": "水中呼吸の矢-延長", "potion": "long_water_breathing", "count": 5},
    {"name": "治癒の矢", "potion": "healing", "count": 5},
    {"name": "治癒の矢-強化", "potion": "strong_healing", "count": 5},
    {"name": "負傷の矢", "potion": "harming", "count": 5},
    {"name": "負傷の矢-強化", "potion": "strong_harming", "count": 5},
    {"name": "毒の矢", "potion": "poison", "count": 5},
    {"name": "毒の矢-延長", "potion": "long_poison", "count": 5},
    {"name": "毒の矢-強化", "potion": "strong_poison", "count": 5},
    {"name": "再生の矢", "potion": "regeneration", "count": 5},
    {"name": "再生の矢-延長", "potion": "long_regeneration", "count": 5},
    {"name": "再生の矢-強化", "potion": "strong_regeneration", "count": 5},
    {"name": "力の矢", "potion": "strength", "count": 5},
    {"name": "力の矢-延長", "potion": "long_strength", "count": 5},
    {"name": "力の矢-強化", "potion": "strong_strength", "count": 5},
    {"name": "弱化の矢", "potion": "weakness", "count": 5},
    {"name": "弱化の矢-延長", "potion": "long_weakness", "count": 5},
    {"name": "幸運の矢", "potion": "luck", "count": 5},
    {"name": "低速落下の矢", "potion": "slow_falling", "count": 5},
    {"name": "低速落下の矢-延長", "potion": "long_slow_falling", "count": 5},
]

# ループで順番に配布
for arrow in arrows:
    m.execute(f'/give @p minecraft:tipped_arrow[minecraft:potion_contents={arrow["potion"]}] {arrow["count"]}')
    m.echo(f'{arrow["name"]}を{arrow["count"]}本配布しました')
