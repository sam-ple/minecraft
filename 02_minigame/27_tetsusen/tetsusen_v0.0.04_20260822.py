# ============================================================
# TETSUSEN GAME SYSTEM
# Version : v0.1.01
# ============================================================


# ============================================================
# STATION SELECT
# ============================================================

on right click on stone button:

    cancel event

    # --------------------------------------------------------
    # ゲーム中は選択不可
    # --------------------------------------------------------

    if {tetsusen.running} is true:

        send "&cゲーム中は焼き場を変更できません。" to player
        stop


    # --------------------------------------------------------
    # ボタン南側のシェルカー
    # --------------------------------------------------------

    set {_shulker} to block south of event-block


    # --------------------------------------------------------
    # 色判定
    # --------------------------------------------------------

    if {_shulker} is red shulker box:

        set {_color} to "red"

    else if {_shulker} is blue shulker box:

        set {_color} to "blue"

    else if {_shulker} is green shulker box:

        set {_color} to "green"

    else if {_shulker} is yellow shulker box:

        set {_color} to "yellow"

    else if {_shulker} is purple shulker box:

        set {_color} to "purple"

    else:

        stop


    # --------------------------------------------------------
    # すでに選択済み
    # --------------------------------------------------------

    if {tetsusen.station::%player%} is set:

        send "&cすでに焼き場を選択しています。" to player
        stop


    # --------------------------------------------------------
    # その色が使用済みか
    # --------------------------------------------------------

    if {tetsusen.station.player::%{_color}%} is set:

        send "&cこの焼き場はすでに選択されています。" to player
        stop


    # --------------------------------------------------------
    # プレイヤーと色を紐付け
    # --------------------------------------------------------

    set {tetsusen.station::%player%} to {_color}

    set {tetsusen.station.player::%{_color}%} to player


    # --------------------------------------------------------
    # シェルカーを保存
    # --------------------------------------------------------

    set {tetsusen.shulker::%player%} to {_shulker}


    # --------------------------------------------------------
    # ボタン削除
    # --------------------------------------------------------

    set event-block to air


    # --------------------------------------------------------
    # メッセージ
    # --------------------------------------------------------

    send "&a%player% が %{_color}%色の焼き場を選択しました。" to all players


# ============================================================
# TETSUSEN COMMAND
# ============================================================

command /tetsusen <text>:

    permission: op

    trigger:

        # ====================================================
        # START
        # ====================================================

        if arg-1 is "start":

            if {tetsusen.running} is true:

                send "&c鉄千はすでに開始しています。"
                stop


            set {tetsusen.running} to true


            # -----------------------------------------------
            # Scoreboard objective
            # -----------------------------------------------

            execute console command "scoreboard objectives add iron_count dummy"


            # -----------------------------------------------
            # 初期値
            # -----------------------------------------------

            loop all players:

                if {tetsusen.shulker::%loop-player%} is set:

                    execute console command "scoreboard players set %loop-player% iron_count 0"


            # -----------------------------------------------
            # Sidebar
            # -----------------------------------------------

            execute console command "scoreboard objectives setdisplay sidebar iron_count"


            send "&a==============================" to all players
            send "&a        鉄千 START!" to all players
            send "&a==============================" to all players

            stop


        # ====================================================
        # STOP
        # ====================================================

        if arg-1 is "stop":

            if {tetsusen.running} is false:

                send "&c鉄千は開始されていません。"
                stop


            set {tetsusen.running} to false


            # -----------------------------------------------
            # Sidebar OFF
            # -----------------------------------------------

            execute console command "scoreboard objectives setdisplay sidebar"


            send "&c==============================" to all players
            send "&c        鉄千 STOP!" to all players
            send "&c==============================" to all players

            stop


        # ====================================================
        # RESET
        # ====================================================

        if arg-1 is "reset":

            set {tetsusen.running} to false


            # -----------------------------------------------
            # 選択情報削除
            # -----------------------------------------------

            delete {tetsusen.station::*}
            delete {tetsusen.station.player::*}
            delete {tetsusen.shulker::*}


            # -----------------------------------------------
            # Scoreboard
            # -----------------------------------------------

            execute console command "scoreboard players reset * iron_count"

            execute console command "scoreboard objectives setdisplay sidebar"


            # -----------------------------------------------
            # 巨大HEAD削除
            # -----------------------------------------------

            execute console command "kill @e[tag=tetsusen_big_head]"


            send "&e鉄千をリセットしました。"

            stop


        # ====================================================
        # UNKNOWN COMMAND
        # ====================================================

        send "&c/tetsusen start"
        send "&c/tetsusen stop"
        send "&c/tetsusen reset"


# ============================================================
# IRON COUNT
# ============================================================

every 1 second:

    # --------------------------------------------------------
    # ゲーム中だけ
    # --------------------------------------------------------

    if {tetsusen.running} is false:

        stop


    # --------------------------------------------------------
    # 全プレイヤー
    # --------------------------------------------------------

    loop all players:

        if {tetsusen.shulker::%loop-player%} is set:

            set {_shulker} to {tetsusen.shulker::%loop-player%}

            set {_iron} to 0


            # -----------------------------------------------
            # シェルカー内の鉄を数える
            # -----------------------------------------------

            loop items in inventory of {_shulker}:

                if loop-item is iron ingot:

                    add amount of loop-item to {_iron}


            # -----------------------------------------------
            # Scoreboard
            # -----------------------------------------------

            execute console command "scoreboard players set %loop-player% iron_count %{_iron}%"
