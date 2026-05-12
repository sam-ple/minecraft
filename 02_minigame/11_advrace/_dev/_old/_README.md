# **Minecraft Advancement Race Game Specification (Advancement Race)**

## 0. Notes

* Instead of command blocks or datapacks, this is being developed with the still relatively niche **Minescript MOD**.
  * Minescript is a MOD that allows you to run Python or Pyjinn (a fusion of Java and Python) inside Minecraft. It only has a client version, not a server version.
* The developer only started Minecraft in April 2025, so their knowledge of Minecraft is still very limited.
  * Also, they have almost no experience with in-game exploration.
* [x] Tested on a free Aternos Minecraft server
  * Server: Vanilla 1.21.8 / Client: Modrinth / Fabric / JE 1.21.8
* [x] Prototype completed
  * Tested only in single-player; multiplayer behavior not yet confirmed
* [x] Purchase additional Minecraft accounts and test with Prism Launcher
* [ ] Conduct pre-tests on Discord

## 1. Overview

* This script implements a mini-game on a Minecraft server where **players compete by earning “Advancements” as points**.
* Players are teleported to randomly selected starting locations, and within the time limit, the player who obtains the most advancements wins.
* At the end of the game, the system displays the rankings and saves logs.

## 2. Game Rules

* The player with the most advancements within the time limit wins.
* Currently, all advancements are worth **1 point**.
  * Extensions: The first player to achieve an advancement gets **+1 bonus point**
  * Extensions: Different points depending on the advancement
  * Extensions: Highlighted advancements with score bonuses
* Variation: Players can prepare in **Creative mode for 30 minutes**, then start the Advancement Race.

## 3. Features

* Start/stop game control
* Countdown timer with boss bar display
* Score management per player (advancement count)
* Logging of each player’s advancement history
* Result announcement (ranking display, log backup)
* Player movement control (lobby, starting locations)
* Chat command-based operation

## 4. Game Flow

1. **Waiting**
   * Players wait in the lobby
   * `--start` begins the game
2. **Game Start**
   * Reset advancements
   * Clear inventories
   * Teleport to random start locations
   * Countdown (3, 2, 1, Start)
   * Switch to Survival mode
3. **Gameplay**
   * Boss bar shows remaining time
   * Each advancement = +1 point
   * Record achievements in a file
   * Notifications via sound/message
     * Achievement sounds may be unnecessary
4. **Game End**
   * Ends when time runs out or with `--stop`
   * Teleport all players back to lobby
   * Switch to Adventure mode
   * Display ranking with colors (1st: Gold, 2nd: Green, 3rd: Aqua)
   * Backup game logs

## 5. Commands

* Currently, any player can use commands
* `--start` : Start the game
* `--stop` : Force stop
* `--settime <seconds>` : Change time limit
* `--status` : Show current game state / remaining time
* `--adv <player>` : Show a player’s advancement history
* `--tp` : Teleport to game’s starting location
  * For players who join mid-game
* `--home` : Teleport to lobby
  * Probably unnecessary, but included just in case
* `--help` : Show list of commands
