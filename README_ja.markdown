goog-starter-kit
================


概要
----
goog-starter-kit は、環境構築が面倒な Closure Library を手軽に
使いはじめるためのツールセットです。
コマンドをひとつ実行するだけで初期設定が終わるので、すぐに開発がはじめられます。
リリース用のコンパイルも、コマンドひとつでOKです。


### 動作環境
以下のプログラムが必要です。
お手元の環境にない場合は、あらかじめインストールしておいてください。

- Git or Subversion ... Closure Library をダウンロードする
- Python .............. Closure Tools を実行する


### ディレクトリ構成
- closure/ ....... ダウンロードした Closure Tools を格納する
- development/ ... 開発用のディレクトリ
- debug/ ......... デバッグ用のディレクトリ(`tools/tools.cfg`の`is_debug_enabled`が`yes`のときのみ存在)
- production/ .... 本番用のディレクトリ
- tools/ ......... 便利なツール群


作業の流れ
----------
1. Closure Tools をダウンロード、配置する

    ターミナルを開き、以下のコマンドを実行します。

        (`goog-starter-kit` ディレクトリに移動してから)
        $ python tools/setup.py

2. `development/` ディレクトリで開発する

    `development/js_dev` ディレクトリ下の既存のコードを修正したり、新たに
    追加したりしてください。

    スクリプトを追加/削除したあとは、依存情報の更新が必要です。
    以下のコマンドを実行してください。

        $ python tools/update_deps.py

3. コンパイルする

    コンパイルすると、パフォーマンス向上や、ソースコードが難読化されるなどの
    利点があります。
    コンパイルするには、以下のコマンドを実行してください。

        $ python tools/compile.py

    コンパイルに成功すると、 `production/` ディレクトリに出力されます。


小技
----
### Mainクラスの名前空間を変更する
Mainクラスの名前空間(初期値は`foo.Main`)を変更するには、`tools/tools.cfg` の
`main_namespace` を変更してください。

変更後は、設定の反映と依存情報の更新をお忘れなく。

    $ python tools/apply_config.py
    $ python tools/update_deps.py


### コンパイル後のファイル名を変更する
`tools/tools.cfg` の `compiled_js` を修正してください。


### ユニットテストを実行する
goog-starter-kit は、 Closure Library のテストツールを利用したユニットテストをサポートしています。
[jsunit の形式](http://www.infoq.com/jp/articles/javascript-tdd) で、簡単にユニットテストを実行できます。

1. [example_test.html](https://github.com/cocopon/goog-starter-kit/blob/master/development/js_dev/example_test.html) をユニットテスト対象と同じディレクトリにコピーする
    
    コピー後、このファイルを `{target_name}_test.html` となるようにリネームします。
    テストファイルの名前は慣例的に `{target_name}_test.html` ですが、 `tool/tools.cfg` の `test_file_pattern` によって変更できます。

2. テストファイルの設定を更新する

    ターミナルを開き、以下のコマンドを実行します。

        (`goog-starter-kit` ディレクトリに移動してから)
        $ python tools/apply_config.py

3. ユニットテストのコードを書く

4. 依存情報を更新する

    以下のコマンドを実行します。

        $ python tools/update_deps.py

5. このファイルをブラウザで開く

    すべてのテストを実行する場合は、 `development/all_tests.html` に **http スキーム** でアクセスしてください (file スキームではうまくいきません)。


### コンパイルしたくないスクリプトがある
`development/js_dev` ディレクトリ以外の場所に配置してください。
本番用では、このディレクトリ内のファイルはすべてコンパイル・統合されたのち、
削除されてしまいます。


### コンパイル後のスクリプトをデバッグする
もし、コンパイル後のスクリプトをデバッグしたければ `tools/tools.cfg` の `is_debug_enabled` を `yes` にしてください。
デバッグが有効だと Source Map や Closure Library のデバッグ機能が動作する `debug/` ディレクトリが作成されます。しかし、コンパイルに時間がかかります。


#### Source Map を使う
goog-starter-kitは Source Map をサポートしており、[Source Map V3](https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit?pli=1) に対応しているブラウザをお使いであれば Source Map を使うことができます。Source Map ファイルは `debug/` ディレクトリに `script.min.js.map` のように保存されます。

ちなみに `production/` ディレクトリに Source Map は **保存されません** 。これは、難読性を保つための措置です。


その他
------
### 作者
cocopon (cocopon@me.com)

### 共同開発者
OrgaChem (orga.chem.job@gmail.com)

### ライセンス
含まれるツールについては、 MIT License で配布しています。
詳細は `LICENSE.txt` を参照してください。
