## Dark Fantasy Scenario Tree: Forbidden Forest

```mermaid
graph TD
    intro[Forbidden Forest Entrance] --> |Enter the mist| mist_path[Mist-shrouded Path]
    intro --> |Return to the village| finale_bad[Despair - BAD END]

    mist_path --> |Follow the whisper| spirit_grove[Spirit Grove]
    mist_path --> |Ignore and press on| cursed_river[Cursed River]
    mist_path --> |Turn back| intro

    spirit_grove --> |Accept the spirit's offer| memory_maze[Memory Maze]
    spirit_grove --> |Refuse and run| cursed_river

    memory_maze --> |Solve the riddle| ancient_ruins[Ancient Ruins]
    memory_maze --> |Fail and lose yourself| finale_loop[Endless Loop - LOOP END]
    memory_maze --> |Recall your past| intro

    cursed_river --> |Cross the river| haunted_village[Haunted Village]
    cursed_river --> |Drink the water| finale_bad2[Corruption - BAD END]

    haunted_village --> |Help the villagers| ancient_ruins
    haunted_village --> |Ignore their pleas| finale_bad3[Lonely Fate - BAD END]
    haunted_village --> |Search for clues| memory_maze

    ancient_ruins --> |Break the curse| finale_good[Freedom - TRUE END]
    ancient_ruins --> |Take the artifact| finale_bad4[Eternal Darkness - BAD END]
    ancient_ruins --> |Return to the forest| mist_path
```

- Each node corresponds to a YAML scenario file in `stories/dark_forest/`.
- The scenario features complex branches, loops, and multiple endings.


## 歯車仕掛けの都市

```mermaid
graph TD
    intro[煙立ち昇る屋根裏工房] --> |街の動力塔へ急行する| tower_plaza[動力塔前の広場]
    intro --> |友人の時計職人レオナに相談する| workshop[時計職人レオナの工房]
    
    tower_plaza --> |衛兵に状況を尋ねる| guildhall[技師ギルド本部]
    tower_plaza --> |蒸気管を調べて異常を探す| undercity[地下蒸気トンネル]
    
    workshop --> |レオナと協力し試作パーツを完成させる| skybridge[上層スカイブリッジ]
    workshop --> |パーツの出処を追うためギルド本部へ向かう| guildhall
    
    guildhall --> |停止案を支持し協力者を募る| archives[記録保管庫]
    guildhall --> |若手派と取引し、上層への通行権を得る| skybridge
    
    skybridge --> |閃光の地点へ急行| undercity
    skybridge --> |制御室のログを解析し原因を突き止める| archives
    
    undercity --> |応急処置で漏れを止め、核心部へ進む| cathedral[歯車大聖堂]
    undercity --> |さらに奥へ進み異常改造の証拠を探す| archives
    
    archives --> |初期設計図を持ち出し、聖堂の制御室へ急ぐ| cathedral
    archives --> |禁断の『自己再起動改造案』で一発逆転を狙う| showdown[中枢制御室]
    
    cathedral --> |地下制御室へ降り、位相リセットを準備する| showdown
    cathedral --> |シスターから都市建設時の秘話を聞き、ヒントを得る| showdown
    
    showdown --> |左レバーを倒し、都市を止める| finale_good[静寂の夜明け - TRUE END]
    showdown --> |右レバーを倒し、賭けに出る| finale_bad[轟音と崩壊 - BAD END]
```

- Each node corresponds to a YAML scenario file in `stories/clockwork_city/`.
- The scenario features complex branches, loops, and multiple endings.

## Villainess Reversal: The Rose of Ruin

```mermaid
graph TD
    intro[The Noble Ball] --> |Scheme against the heroine| confrontation[Confrontation]
    intro --> |Try to befriend the heroine| friendship_path[Friendship Path]
    intro --> |Escape the party| secret_garden[Secret Garden]
    
    confrontation --> |Frame the heroine| downfall[Downfall]
    confrontation --> |Apologize| redemption[Redemption]
    confrontation --> |Get caught| exile[Exile - BAD END]
    
    friendship_path --> |Help the heroine| redemption
    friendship_path --> |Rivalry intensifies| duel[Duel]
    friendship_path --> |Confess your secret| secret_garden

    secret_garden --> |Meet the prince| prince_path[Prince Path]
    secret_garden --> |Discover a hidden letter| time_loop[Time Loop]
    
    prince_path --> |Accept his help| redemption
    prince_path --> |Refuse his help| exile

    duel --> |Win the duel| redemption
    duel --> |Lose the duel| downfall

    downfall --> |Accept your fate| bad_end[Ruined Villainess - BAD END]
    downfall --> |Wish for another chance| time_loop

    redemption --> |Forgive and be forgiven| true_end[True Villainess - TRUE END]
    redemption --> |Sacrifice yourself| secret_end[Secret Ending - SECRET END]

    time_loop --> |Try again| intro
    time_loop --> |Give up| bad_end
```

- Each node corresponds to a YAML scenario file in `stories/villainess_rose/`.
- The scenario features multiple endings, loops, and dramatic reversals.


## 悪役令嬢転生譚 ～薔薇と運命の輪～
```mermaid
graph TD
    intro[貴族の舞踏会] --> |ヒロインを陥れる| confrontation[対決]
    intro --> |ヒロインと友達になる| friendship_path[友情ルート]
    intro --> |会場から逃げ出す| secret_garden[秘密の庭園]
    
    confrontation --> |ヒロインに濡れ衣を着せる| downfall[没落]
    confrontation --> |謝罪する| redemption[贖罪]
    confrontation --> |失敗して捕まる| exile[追放 - バッドエンド]
    
    friendship_path --> |ヒロインを助ける| redemption
    friendship_path --> |ライバル関係が激化| duel[決闘]
    friendship_path --> |秘密を打ち明ける| secret_garden

    secret_garden --> |王子と出会う| prince_path[王子ルート]
    secret_garden --> |謎の手紙を見つける| time_loop[時間遡行]

    prince_path --> |助けを受け入れる| redemption
    prince_path --> |助けを断る| exile

    duel --> |決闘に勝つ| redemption
    duel --> |決闘に負ける| downfall

    downfall --> |運命を受け入れる| bad_end[破滅の令嬢 - バッドエンド]
    downfall --> |やり直しを願う| time_loop

    redemption --> |赦し合う| true_end[真の令嬢 - トゥルーエンド]
    redemption --> |自らを犠牲にする| secret_end[秘密の結末 - シークレットエンド]

    time_loop --> |もう一度挑戦| intro
    time_loop --> |諦める| bad_end
```

- Each node corresponds to a YAML scenario file in `stories/villainess_rose_ja/`.
- The scenario features multiple endings, loops, and dramatic reversals.

