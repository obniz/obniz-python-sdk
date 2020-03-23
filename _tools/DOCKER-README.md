
## コンテナ起動
下記コマンドにて、コンテナを起動する。
working dir は プロジェクトルート

```:ターミナル
$ docker-compose -f ./_tools/docker-compose.yml up -d --build
```

## 使いたいライブラリを追加

### コンテナへ接続
```:ターミナル
$ docker exec -it obniz_python bash
```

### インストール
volumeマウント後にしないといけないのでdockerfileにかけない？

  - pipenv install --deploy --dev

or 
```:ターミナル
$ docker exec -it obniz_python pipenv install --deploy --dev
```


### テスト
  - pipenv run pytest
  
→ test_init.pyの2個だけfailになる（ポートの関係）

or 
```:ターミナル
$ docker exec -it obniz_python pipenv run pytest
```


### 実行
  - pipenv run python xxx.py
or 
```:ターミナル
$ docker exec -it obniz_python pipenv run python xxx.py
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

twine upload --repository pypitest dist/*
OR
twine upload --repository-url https://test.pypi.org/legacy/ dist/*



## testpypiでの動作テスト

pip install --index-url https://test.pypi.org/simple/ obniz

#### docker立ち上げて動くかテスト

```
$ docker-compose -f ./_tools/docker-compose.yml up -d --build
$ docker exec -it obniz_python_prototypetest bash

# docker内
pipenv run python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple obniz
pipenv run python  prototypetest/main.py
```

※バージョン指定する場合は `obniz==0.1.0` にかえる

### repl.itでのテスト

pyproject.tomlに追加してテスト
```
[[tool.poetry.source]]
name = "test-pypi"
url = "https://test.pypi.org/simple/"
```

## アップロード
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
OR
twine upload --repository pypi dist/*
