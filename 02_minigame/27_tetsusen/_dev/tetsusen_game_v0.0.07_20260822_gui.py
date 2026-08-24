# ============================================================
# TETSUSEN ADMIN GUI TEST
# ============================================================

command /tetsusen:

    permission: op

    trigger:

        set {_gui} to chest inventory with 1 row named "&6鉄千管理"

        set slot 1 of {_gui} to emerald named "&a&lSET"
        set lore of slot 1 of {_gui} to "&7焼き場選択モード"

        set slot 3 of {_gui} to diamond named "&e&lSTART"
        set lore of slot 3 of {_gui} to "&7ゲーム開始"

        set slot 5 of {_gui} to redstone named "&c&lSTOP"
        set lore of slot 5 of {_gui} to "&7ゲーム停止"

        set slot 7 of {_gui} to barrier named "&c&lRESET"
        set lore of slot 7 of {_gui} to "&7ゲームリセット"

        open {_gui} to player


# ============================================================
# GUI CLICK
# ============================================================

on inventory click:

    if name of event-inventory is "&6鉄千管理":

        cancel event

        if clicked slot is 1:

            close player's inventory

            send "&aSETを押しました。" to player

        else if clicked slot is 3:

            close player's inventory

            send "&eSTARTを押しました。" to player

        else if clicked slot is 5:

            close player's inventory

            send "&cSTOPを押しました。" to player

        else if clicked slot is 7:

            close player's inventory

            send "&cRESETを押しました。" to player
