# Gamerule[Java Edition]

## チャット・表示系

### announceAdvancements

* 効果：進捗達成をチャットに出すか
* コマンド：`/gamerule announceAdvancements true`

### commandBlockOutput

* 効果：コマンドブロックの実行ログを出すか
* コマンド：`/gamerule commandBlockOutput false`

### logAdminCommands

* 効果：管理コマンドをログに残すか
* コマンド：`/gamerule logAdminCommands false`

### reducedDebugInfo

* 効果：F3情報を制限するか
* コマンド：`/gamerule reducedDebugInfo true`

### sendCommandFeedback

* 効果：コマンド結果をチャットに出すか
* コマンド：`/gamerule sendCommandFeedback false`

### showDeathMessages

* 効果：死亡メッセージを表示するか
* コマンド：`/gamerule showDeathMessages false`

### globalSoundEvents

* 効果：サウンドを全域で聞こえるようにするか
* コマンド：`/gamerule globalSoundEvents true`


## ワールド・時間系

### doDaylightCycle

* 効果：昼夜が進むか
* コマンド：`/gamerule doDaylightCycle false`

### doWeatherCycle

* 効果：天候が変わるか
* コマンド：`/gamerule doWeatherCycle false`

### randomTickSpeed

* 効果：作物成長などの速度（数値）
* コマンド：`/gamerule randomTickSpeed 100`

### snowAccumulationHeight

* 効果：雪が積もる最大層（数値）
* コマンド：`/gamerule snowAccumulationHeight 8`

### spawnRadius

* 効果：初期スポーン範囲（数値）
* コマンド：`/gamerule spawnRadius 0`

### spectatorsGenerateChunks

* 効果：スペクテイターでチャンク生成するか
* コマンド：`/gamerule spectatorsGenerateChunks false`

### lavaSourceConversion

* 効果：溶岩流が溶岩源になるか
* コマンド：`/gamerule lavaSourceConversion true`

### waterSourceConversion

* 効果：水流が水源になるか
* コマンド：`/gamerule waterSourceConversion true`


## ダメージ・生存系

### drowningDamage

* 効果：溺れダメージあるか
* コマンド：`/gamerule drowningDamage false`

### fallDamage

* 効果：落下ダメージあるか
* コマンド：`/gamerule fallDamage false`

### fireDamage

* 効果：炎ダメージあるか
* コマンド：`/gamerule fireDamage false`

### freezeDamage

* 効果：凍結ダメージあるか
* コマンド：`/gamerule freezeDamage false`

### naturalRegeneration

* 効果：自然回復するか
* コマンド：`/gamerule naturalRegeneration false`

### keepInventory

* 効果：死んでも持ち物そのまま
* コマンド：`/gamerule keepInventory true`

### doImmediateRespawn

* 効果：即リスポーンするか
* コマンド：`/gamerule doImmediateRespawn true`

### forgiveDeadPlayers

* 効果：死んだら中立Mobの敵対解除するか
* コマンド：`/gamerule forgiveDeadPlayers true`

### universalAnger

* 効果：中立Mobが全員敵対するか
* コマンド：`/gamerule universalAnger true`

## Mob・スポーン系

### doMobSpawning

* 効果：Mobが自然スポーンするか
* コマンド：`/gamerule doMobSpawning false`

### doMobLoot

* 効果：Mobがアイテム・経験値落とすか
* コマンド：`/gamerule doMobLoot false`

### doEntityDrops

* 効果：エンティティ破壊時にアイテム落とすか
* コマンド：`/gamerule doEntityDrops false`

### doTileDrops

* 効果：ブロック壊したときドロップするか
* コマンド：`/gamerule doTileDrops false`

### doInsomnia

* 効果：ファントムが湧くか
* コマンド：`/gamerule doInsomnia false`

### doPatrolSpawning

* 効果：略奪隊が湧くか
* コマンド：`/gamerule doPatrolSpawning false`

### doTraderSpawning

* 効果：行商人が湧くか
* コマンド：`/gamerule doTraderSpawning false`

### doWardenSpawning

* 効果：ウォーデンが湧くか
* コマンド：`/gamerule doWardenSpawning false`

### mobGriefing

* 効果：Mobがブロック変更できるか
* コマンド：`/gamerule mobGriefing false`

## 爆発・ブロック系

### doFireTick

* 効果：火が燃え広がるか
* コマンド：`/gamerule doFireTick false`

### blockExplosionDropDecay

* 効果：ブロック爆発時のドロップ消失するか
* コマンド：`/gamerule blockExplosionDropDecay false`

### mobExplosionDropDecay

* 効果：Mob爆発時のドロップ消失するか
* コマンド：`/gamerule mobExplosionDropDecay false`

### tntExplosionDropDecay

* 効果：TNT爆発時のドロップ消失するか
* コマンド：`/gamerule tntExplosionDropDecay false`

## 制限・上限系

### commandModificationBlockLimit

* 効果：コマンドで一度に編集できる最大ブロック数（数値）
* コマンド：`/gamerule commandModificationBlockLimit 32768`

### functionCommandLimit

* 効果：一度に実行できるコマンド数の上限（数値）
* コマンド：`/gamerule functionCommandLimit 10000`

### maxCommandChainLength

* 効果：1tickで実行されるコマンド最大数（数値）
* コマンド：`/gamerule maxCommandChainLength 65536`

### maxEntityCramming

* 効果：エンティティ重なり上限（数値）
* コマンド：`/gamerule maxEntityCramming 24`

### playersSleepingPercentage

* 効果：夜スキップに必要な就寝割合（数値）
* コマンド：`/gamerule playersSleepingPercentage 50`

## その他・特殊系

### disableElytraMovementCheck

* 効果：エリトラの速度チェック無効にするか
* コマンド：`/gamerule disableElytraMovementCheck true`

### disableRaids

* 効果：襲撃を無効にするか
* コマンド：`/gamerule disableRaids true`

### doLimitedCrafting

* 効果：レシピ解放済みのみクラフト可能にする
* コマンド：`/gamerule doLimitedCrafting true`

### enderPearlsVanishOnDeath

* 効果：死亡時エンダーパール消えるか
* コマンド：`/gamerule enderPearlsVanishOnDeath true`
