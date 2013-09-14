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


### コンパイルしたくないスクリプトがある
`development/js_dev` ディレクトリ以外の場所に配置してください。
本番用では、このディレクトリ内のファイルはすべてコンパイル・統合されたのち、
削除されてしまいます。


### SourceMap を使う
goog-starter-kitは SourceMap をサポートしており、[SourceMap V3](https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit?pli=1) に対応しているブラウザをお使いであれば SourceMap を使うことができます。


その他
------
### 作者
cocopon (cocopon@me.com)

### 共同開発者
OrgaChem (orga.chem.job@gmail.com)

### ライセンス
含まれるツールについては、 MIT License で配布しています。
詳細は `LICENSE.txt` を参照してください。
