
## コンテナ起動
下記コマンドにて、コンテナを起動する。
working dir は プロジェクトルート

```:ターミナル
$ docker-compose -f ./_tools/docker-compose.yml up -d --build
```

## 使いたいライブラリを追加

### コンテナへ接続
```:ターミナル
$ docker exec -it python3 bash
```

### インストール
volumeマウント後にしないといけないのでdockerfileにかけない？

  - pipenv install --deploy --dev

or 
```:ターミナル
$ docker exec -it python3 pipenv install --deploy --dev
```


### テスト
  - pipenv run pytest
  
→ test_init.pyの2個だけfailになる（ポートの関係）

or 
```:ターミナル
$ docker exec -it python3 pipenv run pytest
```


### 実行
  - pipenv run python xxx.py
or 
```:ターミナル
$ docker exec -it python3 pipenv run python xxx.py
```



## 要らなくなったら...
利用が終わって不要になったらコンテナごと下記コマンドにて削除する。

```:ターミナル
$ docker-compose down
```

#デプロイ

## キャッシュ削除
find . -name \*.pyc -delete

## ファイル作成
python3 setup.py sdist bdist_wheel

## ローカルでpip installテスト
pip install dist/xxxx.whl

**インストール先は`pip show xxx`で確認**

## testアップロード

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

## アップロード
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
