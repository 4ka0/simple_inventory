# Kudamonoya


## 主要なツール
Python 3.7.9<br>
Django 3.1.7<br>
sqlite3


## コードの実行手順
* インストールしたい場所で以下のコマンドを使ってリポジトリをクローンしてください。<br>
`git clone https://github.com/4ka0/kudamonoya.git`
* プロジェクトフォルダに移動してください。<br>
`cd kudamonoya`
* 仮想環境を作って起動してください。<br>
venvを使った例：<br>
`python3 -m venv venv`<br>
`source venv/bin/activate`
* 依存パッケージをインストールしてください。<br>
`pip install -r requirements.txt`
* ローカルサーバーを実行してください。<br>
`python manage.py runserver`
* ブラウザで「localhost:8000」にアクセスしてください。<br>
* 以下の認証情報でログインしてください。<br>
ユーザ名：admin<br>
パスワード：beproud

* プロジェクト・ディレクトリには、販売情報の一括アップロードに使用できる「sales_data.csv」というファイルが含まれていますので、ご利用ください。


## 依存パッケージ

* django-crispy-forms 1.11.1<br>
フォームのスタイル/レイアウトを改善するために使用。<br>
https://github.com/django-crispy-forms/django-crispy-forms

* freezegun 1.1.0<br>
テスト用にdatetimeモジュールをモックするために使用。<br>
https://github.com/spulec/freezegun

* python-dateutil 2.8.1<br>
relativedeltaというモジュールが含まれており、月単位で二つの日付間の差を計算可能（従来のdatetimeのtimedeltaモジュールで使用できるのは日単位までです）。<br>
https://github.com/dateutil/dateutil/

* coverage 5.5<br>
テストコードの範囲を測定するために使用。<br>
https://coverage.readthedocs.io/en/coverage-5.5/


## 注意点

### データベース
* sqlite3を採用したのは、今回のプロジェクトではDBに大量のデータを保存する必要がなく、将来的にデータ量を増やす予定もなく、実際にアプリケーションをデプロイする予定もないためです 。さらに、レビューする皆様がスーパーユーザーや新しい果物オブジェクトを作成する必要性を減らすように、リポジトリに「db.sqlite3」ファイルを含めることにしました。

### SECRET_KEY等の扱い
* 過去の個人プロジェクトでは、django-environやpython-decoupleといったサードパーティのパッケージを使って、SECRET_KEY変数のような情報をコードベースから分離しました。しかし、このプロジェクトを実際にデプロイする予定はなく、また「.env」ファイルを共有する必要をなくすために、今回は情報を分離しないことにしました。

### エラーの扱い
* csvの一括アップロードで、csvファイルの重複エントリ、形式エラーを含むエントリ等は無視されます（静かに失敗します）。

## アピールポイント

### トップページ
* ユーザーのログアウトを可能にするために、ログアウトボタンを追加しました。

### 果物マスタ管理ページ
* 新規果物を追加する時に、同じ名称の果物が既に存在していないかどうかの検証を行います。

### 果物販売管理
* 新規販売情報の追加時に未来の日付が入力できないようにしました。
* csvファイルしかアップロードできないように検証を行います。


## 改善の余地
* 静かに失敗するのではなく、ユーザーにエラーメッセージを出力。
* 販売情報管理ページのテーブルにページネーションを追加。
* 日時の入力フィールドに日付と時間のピッカーを使用。
* 日時の入力フィールドの隣に現在の日時を自動的に入力するボタンを含める。
* selenium等を使ってテストをより徹底したものにする。
* より論理的なタイミングでgitのコミットをする。
* adminのURLを変更する。