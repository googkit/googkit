Closure Library スターターキット
================================


概要
----
Closure Library スターターキット は、Closure Library に不慣れな方向けの
スターターキットです。
このキットを使うことで、初期設定、開発、コンパイルという一連の流れを、
より手軽に行うことができます。


### 動作環境
以下のプログラムが必要です。
お手元の環境にない場合は、あらかじめインストールしておいてください。

- git/svn ... Closure Library をダウンロードする
- python .... Closure Tools を実行する


### ディレクトリ構成
- closure/ ....... ダウンロードした Closure Tools を格納する
- development/ ... 開発用のディレクトリ
- production/ .... 本番用のディレクトリ
- tools/ ......... 便利なツール群


作業の流れ
----------
1. Closure Tools をダウンロード、配置する

    ターミナルを開き、以下のコマンドを実行します。

        (`closure-starter-kit` ディレクトリに移動してから)
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
Mainクラスの名前空間(初期値はcom.mycompany)を変更するには、以下のファイルに
含まれる名前空間をすべて置換してください。

- development/index.html
- development/js_dev/main.js
- tools/compile.py

変更後は、依存情報を更新することをお忘れなく。

    $ python tools/update_deps.py


### コンパイル後のファイル名を変更する
`tools/compile.py` の `COMPILED_JS` を修正してください。


### コンパイルしたくないスクリプトがある
`development/js_dev` ディレクトリ以外の場所に配置してください。
本番用では、このディレクトリ内のファイルはすべてコンパイル・統合されたのち、
削除されてしまいます。


その他
------
### 作者
cocopon (cocopon@me.com)

### ライセンス
MIT License です。詳細については、 `LICENSE.txt` を参照してください。
