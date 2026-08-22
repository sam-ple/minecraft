# ============================================================
# TETSUSEN GAME SYSTEM
# Version : v0.1.02
# ============================================================


# ============================================================
# STATION SELECT
# ============================================================

on right click on stone button:

    cancel event

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
    # 保存
    # --------------------------------------------------------

    set {tetsusen.station::%player%} to {_color}

    set {tetsusen.station.player::%{_color}%} to player

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

command /tetsusen <text> [<number>]:

    permission: op

    trigger:


        # ====================================================
        # START
        # ====================================================

        if arg-1 is "start":

            if {tetsusen.running} is true:

                send "&c鉄千はすでに開始しています。"
                stop


            if arg-2 is not set:

                send "&c使用方法: /tetsusen start <必要個数>"
                send "&7例: /tetsusen start 100"
                stop


            # ------------------------------------------------
            # ゲーム開始
            # ------------------------------------------------

            set {tetsusen.running} to true

            set {tetsusen.required} to arg-2

            set {tetsusen.time} to 0


            # ------------------------------------------------
            # 各プレイヤー初期化
            # ------------------------------------------------

            loop all players:

                if {tetsusen.shulker::%loop-player%} is set:

                    delete {tetsusen.clear::%loop-player%}

                    delete {tetsusen.cleartime::%loop-player%}

                    execute console command "scoreboard players set %loop-player% iron_count 0"


            # ------------------------------------------------
            # Scoreboard
            # ------------------------------------------------

            execute console command "scoreboard objectives add iron_count dummy"

            execute console command "scoreboard objectives setdisplay sidebar iron_count"


            # ------------------------------------------------
            # START TITLE
            # ------------------------------------------------

            send title "&6&lIRON %arg-2%!" with subtitle "&e&lSTART!!" to all players


            # ------------------------------------------------
            # START SOUND
            # ------------------------------------------------

            play sound "block.note_block.pling" with volume 1 and pitch 1 to all players


            # ------------------------------------------------
            # CHAT
            # ------------------------------------------------

            send "&6&l==============================" to all players
            send "&e&l          鉄千 START!" to all players
            send "&f必要個数: &e%{tetsusen.required}%個" to all players
            send "&6&l==============================" to all players

            stop


        # ====================================================
        # STOP
        # ====================================================

        if arg-1 is "stop":

            if {tetsusen.running} is false:

                send "&c鉄千は開始されていません。"
                stop


            set {tetsusen.running} to false


            # ------------------------------------------------
            # Sidebar OFF
            # ------------------------------------------------

            execute console command "scoreboard objectives setdisplay sidebar"


            send "&c&l鉄千 STOP!" to all players

            stop


        # ====================================================
        # RESET
        # ====================================================

        if arg-1 is "reset":

            set {tetsusen.running} to false

            delete {tetsusen.required}
            delete {tetsusen.time}

            delete {tetsusen.station::*}
            delete {tetsusen.station.player::*}
            delete {tetsusen.shulker::*}

            delete {tetsusen.clear::*}
            delete {tetsusen.cleartime::*}


            # ------------------------------------------------
            # Scoreboard
            # ------------------------------------------------

            execute console command "scoreboard players reset * iron_count"

            execute console command "scoreboard objectives setdisplay sidebar"


            # ------------------------------------------------
            # 巨大HEAD削除
            # ------------------------------------------------

            execute console command "kill @e[tag=tetsusen_big_head]"


            send "&e鉄千をリセットしました。"

            stop


        # ====================================================
        # HELP
        # ====================================================

        send "&e/tetsusen start <必要個数>"
        send "&e/tetsusen stop"
        send "&e/tetsusen reset"


# ============================================================
# GAME TIMER
# ============================================================

every 1 second:

    if {tetsusen.running} is true:

        add 1 to {tetsusen.time}


# ============================================================
# IRON COUNT
# ============================================================

every 1 second:

    if {tetsusen.running} is true:

        loop all players:

            if {tetsusen.shulker::%loop-player%} is set:

                # ------------------------------------------------
                # CLEAR済みではない場合のみ
                # ------------------------------------------------

                if {tetsusen.clear::%loop-player%} is not true:

                    set {_shulker} to {tetsusen.shulker::%loop-player%}

                    set {_iron} to 0


                    # --------------------------------------------
                    # 鉄カウント
                    # --------------------------------------------

                    loop items in inventory of {_shulker}:

                        if loop-item is iron ingot:

                            add amount of loop-item to {_iron}


                    # --------------------------------------------
                    # Scoreboard
                    # --------------------------------------------

                    execute console command "scoreboard players set %loop-player% iron_count %{_iron}%"


                    # ============================================
                    # CLEAR CHECK
                    # ============================================

                    if {_iron} >= {tetsusen.required}:

                        set {tetsusen.clear::%loop-player%} to true

                        set {_clearSeconds} to {tetsusen.time}

                        set {tetsusen.cleartime::%loop-player%} to {_clearSeconds}


                        # ----------------------------------------
                        # 時間計算
                        # ----------------------------------------

                        set {_hours} to floor({_clearSeconds} / 3600)

                        set {_minutes} to floor(({_clearSeconds} - ({_hours} * 3600)) / 60)

                        set {_seconds} to {_clearSeconds} - ({_hours} * 3600) - ({_minutes} * 60)


                        # ----------------------------------------
                        # 2桁化
                        # ----------------------------------------

                        if {_minutes} < 10:

                            set {_minText} to "0%{_minutes}%"

                        else:

                            set {_minText} to "%{_minutes}%"


                        if {_seconds} < 10:

                            set {_secText} to "0%{_seconds}%"

                        else:

                            set {_secText} to "%{_seconds}%"


                        set {_timeText} to "%{_hours}%:%{_minText}%:%{_secText}%"


                        # ========================================
                        # CLEAR TITLE
                        # ========================================

                        send title "&6&lCLEAR!!" with subtitle "&f%loop-player% &7%{_timeText}%" to all players


                        # ========================================
                        # SOUND
                        # ========================================

                        play sound "ui.toast.challenge_complete" with volume 1 and pitch 1 to all players

                        play sound "entity.player.levelup" with volume 1 and pitch 1 to loop-player


                        # ========================================
                        # PARTICLE
                        # ========================================

                        execute console command "particle minecraft:firework ~ ~2 ~ 1 1 1 0.2 50 force %loop-player%"


                        # ========================================
                        # CHAT
                        # ========================================

                        send "" to all players
                        send "&6&l====================================" to all players
                        send "&e&l              CLEAR!!" to all players
                        send "&f%loop-player% &7→ &e%{_timeText}%" to all players
                        send "&6&l====================================" to all players
                        send "" to all players
