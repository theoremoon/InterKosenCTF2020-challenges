# InterKosenCTF2020

- `task.json` が存在するディレクトリが問題のディレクトリとして扱われる
  + 問題のディレクトリは `category/title/` にする
- `distfiles` に配置したファイルはtar.gzに纏めて配布される
- `rawdistfiles` に配置したファイルはそのまま配布される
- デプロイが必要な場合には `docker-compose.yml` に全てを書く
  + `docker-compose.yml`では `image` と `volumes`, `container_name` は使えない
- solvability checkを行う問題は `solution/docker-compose.yml` を配置する
  + service名は必ず`solve`にする
  + `docker-compose run -e HOST=$HOST -e PORT=$PORT` のように問題サーバの情報が渡される
  
### 複数インスタンスを立ち上げて良い時

Web問題でDBは一つにしたいがフロントは複数立ち上げられる、みたいな場合に docker-compose にreplica数を書いておいてくれると良い
```yml
services:
  hoge_service:
    ...
    deploy:
      mode: replicated
      replicas: 6
    ...
```

## category/title/task.json

```json
{
  "name": "challenge_name",
  "description": "<p>challenge description. it is html<br /> <pre>nc ${host} $port </pre> </p>",
  "flag": "KosenCTF{some_awesome_flag_wowow_takoyaki}",
  "author": "author name",
  "tags": ["crypto", "warmup"],
  "host": "pwn.kosenctf.com",
  "port": 8080,
  "is_survey": false
}
```

- host / port は省略可
- "descritpion"内でhost/portのような変数を使いたい場合は`${host}`か`$host`とする。
  + 詳しくは [string.Template](https://docs.python.org/ja/3/library/string.html#string.Template) をみて
  + host/port以外の変数も使える


## Dockerfile
動かすプログラムに応じて次のコンテナを優先して使う。（上にくるほど優先度高。他にあったら追記して。）

- python:3.7-alpine
- php:7.4.1-fpm-alpine
- ubuntu:18.04

問題設定的にどうしても他のバージョンが必要な場合は他のコンテナを使っても良い。
（例:Flask問だが`LD_PRELOAD`などのハックが必要なのでubuntuコンテナを使う、など。）
