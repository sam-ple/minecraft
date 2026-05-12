import minescript as m
import math

def spawn_big_head():

    px, py, pz = m.player_position()
    x = math.floor(px)
    y = math.floor(py) + 30
    z = math.floor(pz) + 5

    # 召喚
    m.execute(
        f'/summon minecraft:item_display {x} {y} {z} '
        f'{{item:{{"id":"minecraft:player_head",count:1,'
        f'components:{{"minecraft:profile":{{name:"crocadooo"}}}}}},'
        f'Tags:["big_player_head"]}}'
    )

    # スケール変更（50倍）
    m.execute(
        '/data modify entity '
        '@e[tag=big_player_head,sort=nearest,limit=1] '
        # 'transformation.scale set value [50f,50f,50f]'
        # 'transformation.scale set value [8f,8f,8f]'
        'transformation.scale set value [8f,8f,1f]'
    )

    m.echo("Big crocadooo head spawned.")

if __name__ == "__main__":
    spawn_big_head()
