# LINE Notify

LINE通知アプリケーション

大学のポータルシステムに来る重要通知をクローリング・スクレイピングして更新があった場合にLINEに通知を送ります

## 使用技術
- Scrapy
- Splash
- LINE Notify API
- iPython
- Docker
- flake8
- GitHub Actions

## getting start

```
docker-compose up --build
```

## 実行コマンド

コンテナに入る

```
dokcer-compose run line-notify bash
```

クローラー開始コマンド

```
scrapy crawl notify_spider -o result.json --logfile result.log
```

## テスト

```
falke8 ./
```




