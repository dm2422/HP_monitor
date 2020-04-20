# HP_MONITOR
ホームページの変更を検知して各プラットフォームに配信する機能を提供します。

# 特徴
* 全てのモジュールが独立しているため、サイトやプラットフォームの追加が簡単にできます。
* 簡単なトークンの管理を提供します。

# Requirements
* Python3.8
* cronのような定期実行サービス

# 注意
このモジュールでは、誤配信を防ぐために、`-O`オプションをつけないとデバッグモードで起動され、配信されないようになっています。

# 初期設定
## Linux/mac
```shell script
python3.8 venv venv # 仮想環境の構築
./venv/bin/python -m pip install -r requirements.txt # 要求モジュールをインストール
./venv/bin/python manage.py init # 履歴の初期化
```
## Windows
```shell script
python3.8 venv venv # 仮想環境の構築
venv\Scripts\python -m pip install -r requirements.txt # 要求モジュールをインストール
venv\Scripts\python manage.py init
```

# 定期実行設定例
## cron
```text
* * * * * cd /home/user/HP_monitor;./venv/bin/python -O main.py
```

# サイトの追加方法
詳しいドキュメントは後日追記します。

1. `crawlers.schools`に監視したいサイトのクローラを追加します。
2. `tokens.json`に配信用のトークンを設定します。
3. `python manage.py init`を実行して、現在のサイトの状態をキャッシュします。

# プラットフォームの追加方法
詳しいドキュメントは後日追記します。

1. `API.agents`にAPIのエージェントを実装します。
2. `tokens.schema.json`にトークンの型を設定します。
3. `tokens.json`にトークンを設定します。

# `tokens.json`の記述方法
ここに書かれているトークンはサンプルのために生成した乱数です。有効なトークンではありません。

## `shared`
`use_shared`がトークンに指定されているサイトでは、このトークンを使用します。

## サイトごとのトークン
`null`を指定した場合、配信は行われません。

## 簡単な例
```json
{
  "shared":{
    "twitter":{
      "consumer_key":"wxwCk9)Qn%t@5C*#UUT!rbcXe",
      "consumer_secret":"_OZIB8KQAqXwkNKD*H#evjAIg7TOO36Tt51g*7UmeCVC&K6i!2",
      "access_token":"hr!hKC!Pl)30Fw$R&7jtYDLcyCsjufT!6oI2cP^&r%7T^LyxEg",
      "access_token_secret":"O1MD6!Wh(CGhtMV1uAC9k@SxWd(3m*Oz*p1i5czBmO1!f"
    },
    "line":{
      "channel_token":"R^gQ58klCSn(Wzlet^1jN2g&IDdh8hp#&IAllW@LT5z5ASCnMxf5$_B8e)QEAs00W3@$ncQv8Uzec#%Qy)lcWeaz7^CFe5X!)@T&$yV25GXhB!5+rg3w%whRhHKKnIo7M!dIJQ_qbvfC#Q*bmNZKAn9ne76KyYzPMrjLih3ycAS%"
    }
  },
  "合同会社笹田運輸":{
    "twitter":{
      "consumer_key":"JlB%#9cK*NvNNUkh9dOYpOzjK",
      "consumer_secret":"eEq1Q)9mgvAbk7op_xK3UpKtC#@29g)@4a*CiNvkAQ6c1cq9RE",
      "access_token":"^He@VhEZm^9)xQXy(%!ktN#V(g+18FWwQq40^2i1e^NLHs^4Ox",
      "access_token_secret":"mNqRT7NGn_KywJbf6jNopQE@RWQx_dEq5lYxefy5BgLMc"
    },
    "line":"use_shared"
  },
  "原田運輸有限会社":{
    "twitter":"use_shared",
    "line":"use_shared"
  },
  "株式会社田辺建設":{
    "twitter":null,
    "line":{
      "channel_token":")biElxtaJCQI)zSf0IablymP_&@i!ue&a9VbVf@yQZZCQJzWLV!7F!^$gUgy%xdBvh1rCNp)LBPv1qXOp(lK)BmBy7ZYXbqIdVt6fYkyTJFkScmUmzkU7oZlaK()@G)icr*(x*W9R&#^xEH5L8Fc7N*kq9hBb^0muTH5wSjWQ+2X"
    }
  }
}
```
