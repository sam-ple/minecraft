# ============================================================
# TETSUSEN GAME SYSTEM
# Version : v0.3.01
#
# Command
#   /tetsusen
#
# GUI
#   SET
#   START
#   STOP
#   RESET
#
# ============================================================


# ============================================================
# LOAD
# ============================================================

on load:

    set {tetsusen.running} to false
    set {tetsusen.setup} to false


# ============================================================
# OPEN TETSUSEN GUI
# ============================================================

command /tetsusen:

    permission: op

    trigger:

        set {_gui} to chest inventory with 1 row named "&6鉄千管理"


        # ----------------------------------------------------
        # SET
        # ----------------------------------------------------

        set slot 1 of {_gui} to emerald named "&a&lSET"
        set lore of slot 1 of {_gui} to "&7焼き場選択モードを開始"


        # ----------------------------------------------------
        # START
        # ----------------------------------------------------

        set slot 3 of {_gui} to diamond named "&e&lSTART"
        set lore of slot 3 of {_gui} to "&7必要個数を選択してゲーム開始"


        # ----------------------------------------------------
        # STOP
        # ----------------------------------------------------

        set slot 5 of {_gui} to redstone named "&c&lSTOP"
        set lore of slot 5 of {_gui} to "&7ゲーム停止"


        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        set slot 7 of {_gui} to barrier named "&c&lRESET"
        set lore of slot 7 of {_gui} to "&7焼き場・ゲームを初期化"


        open {_gui} to player


# ============================================================
# ADMIN GUI CLICK
# ============================================================

on inventory click:

    # ========================================================
    # MAIN GUI
    # ========================================================

    if name of event-inventory is "&6鉄千管理":

        cancel event


        # ====================================================
        # SET
        # ====================================================

        if clicked slot is 1:

            close player's inventory


            # ------------------------------------------------
            # ゲーム中
            # ------------------------------------------------

            if {tetsusen.running} is true:

                send "&cゲーム中はSETできません。" to player
                stop


            # ------------------------------------------------
            # 既にSET中
            # ------------------------------------------------

            if {tetsusen.setup} is true:

                send "&eすでに焼き場選択モードです。" to player
                stop


            # ------------------------------------------------
            # SET開始
            # ------------------------------------------------

            set {tetsusen.setup} to true


            # ------------------------------------------------
            # CLEAR状態初期化
            # ------------------------------------------------

            delete {tetsusen.clear::*}
            delete {tetsusen.cleartime::*}


            # ------------------------------------------------
            # MESSAGE
            # ------------------------------------------------

            send "" to all players
            send "&a&l==============================" to all players
            send "&a&l          鉄千 SET" to all players
            send "&e焼き場を選択してください。" to all players
            send "&a&l==============================" to all players
            send "" to all players

            stop


        # ====================================================
        # START
        # ====================================================

        if clicked slot is 3:

            close player's inventory


            # ------------------------------------------------
            # SET確認
            # ------------------------------------------------

            if {tetsusen.setup} is not true:

                send "&c先にSETを行ってください。" to player
                stop


            # ------------------------------------------------
            # 既に開始済み
            # ------------------------------------------------

            if {tetsusen.running} is true:

                send "&c鉄千はすでに開始しています。" to player
                stop


            # ------------------------------------------------
            # 必要個数GUI
            # ------------------------------------------------

            set {_gui} to chest inventory with 1 row named "&6必要個数を選択"


            set slot 1 of {_gui} to iron ingot named "&f&l50個"
            set lore of slot 1 of {_gui} to "&750個でCLEAR"


            set slot 2 of {_gui} to iron ingot named "&f&l100個"
            set lore of slot 2 of {_gui} to "&7100個でCLEAR"


            set slot 3 of {_gui} to iron ingot named "&f&l150個"
            set lore of slot 3 of {_gui} to "&7150個でCLEAR"


            set slot 4 of {_gui} to iron ingot named "&f&l200個"
            set lore of slot 4 of {_gui} to "&7200個でCLEAR"


            set slot 5 of {_gui} to iron ingot named "&f&l300個"
            set lore of slot 5 of {_gui} to "&7300個でCLEAR"


            set slot 6 of {_gui} to iron ingot named "&f&l500個"
            set lore of slot 6 of {_gui} to "&7500個でCLEAR"


            open {_gui} to player

            stop


        # ====================================================
        # STOP
        # ====================================================

        if clicked slot is 5:

            close player's inventory


            if {tetsusen.running} is false:

                send "&c鉄千は開始されていません。" to player
                stop


            set {tetsusen.running} to false


            # ------------------------------------------------
            # Sidebar OFF
            # ------------------------------------------------

            execute console command "scoreboard objectives setdisplay sidebar"


            # ------------------------------------------------
            # MESSAGE
            # ------------------------------------------------

            send "" to all players
            send "&c&l==============================" to all players
            send "&c&l          鉄千 STOP!" to all players
            send "&c&l==============================" to all players
            send "" to all players

            stop


        # ====================================================
        # RESET
        # ====================================================

        if clicked slot is 7:

            close player's inventory


            # ------------------------------------------------
            # ゲーム停止
            # ------------------------------------------------

            set {tetsusen.running} to false
            set {tetsusen.setup} to false


            # ------------------------------------------------
            # 選択済みプレイヤーごとに復元
            #
            # v0.2.03で動作確認済みの処理をそのまま使用
            # ------------------------------------------------

            loop all players:

                if {tetsusen.shulker::%loop-player%} is set:

                    set {_shulker} to {tetsusen.shulker::%loop-player%}


                    # =================================================
                    # NORMAL HEAD REMOVE
                    #
                    # 現行仕様:
                    # shulker + Y1
                    # =================================================

                    set {_headLocation} to location of {_shulker}

                    add 1 to y-coordinate of {_headLocation}

                    set block at {_headLocation} to air


                    # =================================================
                    # BUTTON RESTORE
                    #
                    # ★ 動作確認済み v0.2.03 と同じ
                    #
                    # shulker
                    #   ↓ Z-1
                    # button
                    # =================================================

                    set {_buttonLocation} to location of {_shulker}

                    remove 1 from z-coordinate of {_buttonLocation}

                    set block at {_buttonLocation} to stone button


            # =================================================
            # BIG HEAD REMOVE
            # =================================================

            execute console command "kill @e[tag=tetsusen_big_head]"


            # =================================================
            # SCOREBOARD
            # =================================================

            execute console command "scoreboard players reset * iron_count"

            execute console command "scoreboard objectives setdisplay sidebar"


            # =================================================
            # VARIABLES CLEAR
            # =================================================

            delete {tetsusen.station::*}
            delete {tetsusen.station.player::*}
            delete {tetsusen.shulker::*}

            delete {tetsusen.button::*}
            delete {tetsusen.head::*}
            delete {tetsusen.bighead.location::*}

            delete {tetsusen.required}
            delete {tetsusen.time}

            delete {tetsusen.clear::*}
            delete {tetsusen.cleartime::*}


            # =================================================
            # MESSAGE
            # =================================================

            send "" to all players
            send "&e&l==============================" to all players
            send "&e&l          鉄千 RESET" to all players
            send "&f焼き場・プレイヤーヘッド・ボタンを初期化しました。" to all players
            send "&e&l==============================" to all players
            send "" to all players

            stop


# ============================================================
# REQUIRED COUNT GUI
# ============================================================

on inventory click:

    if name of event-inventory is "&6必要個数を選択":

        cancel event


        # ====================================================
        # REQUIRED COUNT
        # ====================================================

        if clicked slot is 1:

            set {_required} to 50

        else if clicked slot is 2:

            set {_required} to 100

        else if clicked slot is 3:

            set {_required} to 150

        else if clicked slot is 4:

            set {_required} to 200

        else if clicked slot is 5:

            set {_required} to 300

        else if clicked slot is 6:

            set {_required} to 500

        else:

            stop


        # ====================================================
        # CLOSE GUI
        # ====================================================

        close player's inventory


        # ====================================================
        # GAME START
        #
        # 元 v0.2.03 の START 処理
        # ====================================================

        set {tetsusen.running} to true

        set {tetsusen.required} to {_required}

        set {tetsusen.time} to 0


        # ====================================================
        # PLAYER STATE INITIALIZATION
        # ====================================================

        loop all players:

            if {tetsusen.shulker::%loop-player%} is set:

                delete {tetsusen.clear::%loop-player%}

                delete {tetsusen.cleartime::%loop-player%}

                execute console command "scoreboard players set %loop-player% iron_count 0"


        # ====================================================
        # SCOREBOARD
        # ====================================================

        execute console command "scoreboard objectives add iron_count dummy"

        execute console command "scoreboard objectives setdisplay sidebar iron_count"


        # ====================================================
        # START TITLE
        # ====================================================

        send title "&6&lIRON %{tetsusen.required}%!" with subtitle "&e&lSTART!!" to all players


        # ====================================================
        # SOUND
        # ====================================================

        play sound "block.note_block.pling" with volume 1 and pitch 1 to all players


        # ====================================================
        # CHAT
        # ====================================================

        send "" to all players
        send "&6&l==============================" to all players
        send "&e&l          鉄千 START!" to all players
        send "&f必要個数: &e%{tetsusen.required}%個" to all players
        send "&6&l==============================" to all players
        send "" to all players


# ============================================================
# STATION SELECT
# ============================================================

on right click on stone button:

    cancel event


    # --------------------------------------------------------
    # SETモードでない場合
    # --------------------------------------------------------

    if {tetsusen.setup} is not true:

        stop


    # --------------------------------------------------------
    # ゲーム中は選択不可
    # --------------------------------------------------------

    if {tetsusen.running} is true:

        send "&cゲーム中は焼き場を変更できません。" to player
        stop


    # --------------------------------------------------------
    # ボタンの南側にあるシェルカーを取得
    #
    # MineScript:
    #
    #   button  = Z-1
    #   shulker = Z
    #
    # --------------------------------------------------------

    set {_shulker} to block south of event-block


    # --------------------------------------------------------
    # シェルカーの色判定
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
    # プレイヤーがすでに選択済み
    # --------------------------------------------------------

    if {tetsusen.station::%player%} is set:

        send "&cすでに焼き場を選択しています。" to player
        stop


    # --------------------------------------------------------
    # その色がすでに使用されている
    # --------------------------------------------------------

    if {tetsusen.station.player::%{_color}%} is set:

        send "&cこの焼き場はすでに選択されています。" to player
        stop


    # ========================================================
    # SAVE
    # ========================================================

    # プレイヤー → 色
    set {tetsusen.station::%player%} to {_color}


    # 色 → プレイヤー
    set {tetsusen.station.player::%{_color}%} to player


    # プレイヤー → シェルカー
    set {tetsusen.shulker::%player%} to {_shulker}


    # ========================================================
    # NORMAL PLAYER HEAD LOCATION
    #
    # 現在の実動作版 v0.2.03 と同じ
    #
    # X     = shulker X
    # Y + 1 = shulker Y + 1
    # Z     = shulker Z
    # ========================================================

    set {_headLocation} to location of {_shulker}

    add 1 to y-coordinate of {_headLocation}

    set {tetsusen.head::%player%} to {_headLocation}


    # ========================================================
    # BIG PLAYER HEAD LOCATION
    #
    # X     = shulker X
    # Y +10 = shulker Y + 10
    # Z + 2 = shulker Z + 2
    # ========================================================

    set {_bigLocation} to location of {_shulker}

    add 10 to y-coordinate of {_bigLocation}

    add 2 to z-coordinate of {_bigLocation}

    set {tetsusen.bighead.location::%player%} to {_bigLocation}


    # ========================================================
    # DELETE BUTTON
    # ========================================================

    set event-block to air


    # ========================================================
    # NORMAL PLAYER HEAD
    # ========================================================

    set block at {_headLocation} to player head

    set skull owner of block at {_headLocation} to player


    # ========================================================
    # BIG PLAYER HEAD
    # ========================================================

    set {_bigX} to x-coordinate of {_bigLocation}

    set {_bigY} to y-coordinate of {_bigLocation}

    set {_bigZ} to z-coordinate of {_bigLocation}


    execute console command "summon minecraft:item_display %{_bigX}% %{_bigY}% %{_bigZ}% {item:{id:""minecraft:player_head"",count:1,components:{""minecraft:profile"":{name:""%player%""}}},billboard:""fixed"",Tags:[""tetsusen_big_head""]}"


    # ========================================================
    # BIG HEAD SCALE
    # ========================================================

    execute console command "data modify entity @e[tag=tetsusen_big_head,x=%{_bigX}%,y=%{_bigY}%,z=%{_bigZ}%,distance=..1,limit=1] transformation.scale set value [6f,6f,1f]"


    # ========================================================
    # MESSAGE
    # ========================================================

    send "&a%player% が %{_color}%色の焼き場を選択しました。" to all players


# ============================================================
# GAME TIMER + IRON COUNT + CLEAR
# ============================================================

every 1 second:

    if {tetsusen.running} is true:


        # ====================================================
        # TIMER
        # ====================================================

        add 1 to {tetsusen.time}


        # ====================================================
        # PLAYER LOOP
        # ====================================================

        loop all players:

            if {tetsusen.shulker::%loop-player%} is set:


                # =================================================
                # CLEAR済みではない場合のみ
                # =================================================

                if {tetsusen.clear::%loop-player%} is not true:

                    set {_shulker} to {tetsusen.shulker::%loop-player%}

                    set {_iron} to 0


                    # ============================================
                    # IRON COUNT
                    # ============================================

                    loop items in inventory of {_shulker}:

                        if loop-item is iron ingot:

                            add amount of loop-item to {_iron}


                    # ============================================
                    # SCOREBOARD
                    # ============================================

                    execute console command "scoreboard players set %loop-player% iron_count %{_iron}%"


                    # ============================================
                    # CLEAR CHECK
                    # ============================================

                    if {_iron} >= {tetsusen.required}:

                        set {tetsusen.clear::%loop-player%} to true

                        set {_clearSeconds} to {tetsusen.time}

                        set {tetsusen.cleartime::%loop-player%} to {_clearSeconds}


                        # ========================================
                        # TIME CALCULATION
                        # ========================================

                        set {_hours} to floor({_clearSeconds} / 3600)

                        set {_minutes} to floor(({_clearSeconds} - ({_hours} * 3600)) / 60)

                        set {_seconds} to {_clearSeconds} - ({_hours} * 3600) - ({_minutes} * 60)


                        # ----------------------------------------
                        # MINUTES
                        # ----------------------------------------

                        if {_minutes} < 10:

                            set {_minText} to "0%{_minutes}%"

                        else:

                            set {_minText} to "%{_minutes}%"


                        # ----------------------------------------
                        # SECONDS
                        # ----------------------------------------

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

                        execute console command "execute at %loop-player% run particle minecraft:firework ~ ~2 ~ 1 1 1 0.2 50 force"


                        # ========================================
                        # CHAT
                        # ========================================

                        send "" to all players
                        send "&6&l====================================" to all players
                        send "&e&l              CLEAR!!" to all players
                        send "&f%loop-player% &7→ &e%{_timeText}%" to all players
                        send "&6&l====================================" to all players
                        send "" to all players
