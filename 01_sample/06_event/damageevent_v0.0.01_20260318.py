# import minescript as m
# from minescript import EventQueue, EventType
# import pprint

# with EventQueue() as eq:
#     eq.register_damage_listener()

#     m.echo("⚡ DamageEvent DEBUG START")

#     while True:
#         event = eq.get()

#         if event.type != EventType.DAMAGE:
#             continue

#         m.echo("----- DAMAGE EVENT RAW -----")

#         # 全フィールド表示
#         pprint.pprint(event.__dict__)

#         # 一応よく使うやつも表示
#         m.echo(f"entity_uuid: {event.entity_uuid}")
#         m.echo(f"cause_uuid : {event.cause_uuid}")
#         m.echo(f"source     : {event.source}")

プレイヤーのみに限定する場合
import minescript as m
from minescript import EventQueue, EventType
import pprint

with EventQueue() as eq:
    eq.register_damage_listener()

    m.echo("⚡ DamageEvent (Players Only)")

    while True:
        event = eq.get()

        if event.type != EventType.DAMAGE:
            continue

        # --- プレイヤー判定 ---
        victim = m.players(uuid=event.entity_uuid)
        attacker = m.players(uuid=event.cause_uuid) if event.cause_uuid else []

        # どちらもプレイヤーじゃなければスキップ
        if not victim and not attacker:
            continue

        m.echo("----- PLAYER DAMAGE EVENT -----")

        pprint.pprint(event.__dict__)

        if victim:
            m.echo(f"victim   : {victim[0].name}")
        if attacker:
            m.echo(f"attacker : {attacker[0].name}")

        m.echo(f"source   : {event.source}")


[2026-03-18 22:04:46] 🟢 Chat logging START
[2026-03-18 22:04:48] ⚡ DamageEvent (Players Only)
[2026-03-18 22:04:54] ----- PLAYER DAMAGE EVENT -----
[2026-03-18 22:04:54] victim   : saaample
[2026-03-18 22:04:54] attacker : crocadooo
[2026-03-18 22:04:54] source   : player
[2026-03-18 22:04:55] {'cause_uuid': '395e65fc-d71b-45c0-adb2-3f4afde04449',
[2026-03-18 22:04:55]  'entity_uuid': 'a96ccb39-9e07-47c7-8274-23fa7b69509e',
[2026-03-18 22:04:55]  'source': 'player',
[2026-03-18 22:04:55]  'time': 1773839094.963,
[2026-03-18 22:04:55]  'type': 'damage'}
[2026-03-18 22:05:43] crocadooo has made the advancement [A Throwaway Joke]
[2026-03-18 22:05:43] ----- PLAYER DAMAGE EVENT -----
[2026-03-18 22:05:43] victim   : saaample
[2026-03-18 22:05:43] attacker : crocadooo
[2026-03-18 22:05:43] source   : trident
[2026-03-18 22:05:43] {'cause_uuid': '395e65fc-d71b-45c0-adb2-3f4afde04449',
[2026-03-18 22:05:43]  'entity_uuid': 'a96ccb39-9e07-47c7-8274-23fa7b69509e',
[2026-03-18 22:05:43]  'source': 'trident',
[2026-03-18 22:05:43]  'time': 1773839143.863,
[2026-03-18 22:05:43]  'type': 'damage'}
[2026-03-18 22:06:05] ----- PLAYER DAMAGE EVENT -----
[2026-03-18 22:06:05] victim   : saaample
[2026-03-18 22:06:05] attacker : crocadooo
[2026-03-18 22:06:05] source   : player
[2026-03-18 22:06:05] {'cause_uuid': '395e65fc-d71b-45c0-adb2-3f4afde04449',
[2026-03-18 22:06:05]  'entity_uuid': 'a96ccb39-9e07-47c7-8274-23fa7b69509e',
[2026-03-18 22:06:05]  'source': 'player',
[2026-03-18 22:06:05]  'time': 1773839165.209,
[2026-03-18 22:06:05]  'type': 'damage'}
[2026-03-18 22:06:26] ----- PLAYER DAMAGE EVENT -----
[2026-03-18 22:06:26] victim   : saaample
[2026-03-18 22:06:26] attacker : crocadooo
[2026-03-18 22:06:26] source   : player
[2026-03-18 22:06:26] {'cause_uuid': '395e65fc-d71b-45c0-adb2-3f4afde04449',
[2026-03-18 22:06:26]  'entity_uuid': 'a96ccb39-9e07-47c7-8274-23fa7b69509e',
[2026-03-18 22:06:26]  'source': 'player',
[2026-03-18 22:06:26]  'time': 1773839186.628,
[2026-03-18 22:06:26]  'type': 'damage'}
[2026-03-18 22:06:44] ----- PLAYER DAMAGE EVENT -----
[2026-03-18 22:06:44] victim   : crocadooo
[2026-03-18 22:06:44] attacker : saaample
[2026-03-18 22:06:44] source   : player
[2026-03-18 22:06:44] {'cause_uuid': 'a96ccb39-9e07-47c7-8274-23fa7b69509e',
[2026-03-18 22:06:44]  'entity_uuid': '395e65fc-d71b-45c0-adb2-3f4afde04449',
[2026-03-18 22:06:44]  'source': 'player',
[2026-03-18 22:06:44]  'time': 1773839204.415,
[2026-03-18 22:06:44]  'type': 'damage'}
[2026-03-18 22:07:07] saaample has made the advancement [A Throwaway Joke]
[2026-03-18 22:07:07] ----- PLAYER DAMAGE EVENT -----
[2026-03-18 22:07:07] victim   : crocadooo
[2026-03-18 22:07:07] attacker : saaample
[2026-03-18 22:07:07] source   : trident
[2026-03-18 22:07:07] {'cause_uuid': 'a96ccb39-9e07-47c7-8274-23fa7b69509e',
[2026-03-18 22:07:07]  'entity_uuid': '395e65fc-d71b-45c0-adb2-3f4afde04449',
[2026-03-18 22:07:07]  'source': 'trident',
[2026-03-18 22:07:07]  'time': 1773839227.314,
[2026-03-18 22:07:07]  'type': 'damage'}
[2026-03-18 22:07:22] saaample has made the advancement [Take Aim]
[2026-03-18 22:07:22] ----- PLAYER DAMAGE EVENT -----
[2026-03-18 22:07:22] victim   : crocadooo
[2026-03-18 22:07:22] attacker : saaample
[2026-03-18 22:07:22] source   : arrow
[2026-03-18 22:07:23] {'cause_uuid': 'a96ccb39-9e07-47c7-8274-23fa7b69509e',
[2026-03-18 22:07:23]  'entity_uuid': '395e65fc-d71b-45c0-adb2-3f4afde04449',
[2026-03-18 22:07:23]  'source': 'arrow',
[2026-03-18 22:07:23]  'time': 1773839242.954,
[2026-03-18 22:07:23]  'type': 'damage'}

