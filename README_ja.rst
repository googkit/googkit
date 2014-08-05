Googkit
=======


.. image:: https://pypip.in/version/googkit/badge.svg
   :target: https://crate.io/packages/googkit

.. image:: https://travis-ci.org/googkit/googkit.svg?branch=master
    :target: https://travis-ci.org/googkit/googkit




概要
----
Googkit は、Closure Library を利用したWebアプリケーション開発を支援するツール
です。わずか2ステップでプロジェクトが作成でき、すぐに開発がはじめられます。
面倒な設定が必要だったコンパイルも、コマンド一発でOKです。


動作環境
~~~~~~~~
以下のプログラムが必要です。
お手元の環境にない場合は、あらかじめインストールしておいてください。

:Git:    Closure Library をダウンロードする
:Python: Closure Tools を実行する




Googkitのインストール
---------------------
はじめに、Googkit をインストールします。


LinuxまたはOS X
~~~~~~~~~~~~~~~

1. `Googkit の最新版 <https://github.com/googkit/googkit/releases>`_ をダウンロード・展開する


2. お好みの場所に移動する::

     $ mv googkit /opt


3. 環境変数の ``PATH`` に追加する::

     export GOOGKIT_HOME=/opt/googkit
     export PATH=$PATH:$GOOGKIT_HOME/bin


Windows
~~~~~~~

1. `Googkit の最新版 <https://github.com/googkit/googkit/releases>`_ をダウンロード・展開する


2. お好みの場所に移動する::

     $ move googkit C:\


3. 環境変数を追加する

   +------------------+--------------------------------------+
   | Variable         | Value                                |
   +------------------+--------------------------------------+
   | ``GOOGKIT_HOME`` | ``C:\googkit``                       |
   +------------------+--------------------------------------+
   | ``PATH``         | ``;%GOOGKIT_HOME%\bin`` を末尾に追加 |
   +------------------+--------------------------------------+




作業の流れ
----------
1. プロジェクト用のディレクトリを作成し、初期化する::

     $ mkdir my_project
     $ cd my_project
     $ googkit init


2. Closure Tools をダウンロードする::

     $ googkit setup


3. ``development/`` ディレクトリで開発する

   ``development/js_dev`` ディレクトリ内で開発します。

   スクリプトを追加/削除したあとは、依存情報を更新します::

     $ googkit ready


4. プロジェクトをビルドする

   ビルドするとJavaScriptファイルがコンパイルされ、パフォーマンスが向上し、
   ソースコードが難読化されるなどの利点があります::

     $ googkit build

   ビルドに成功すると、 ``production/`` ディレクトリが作成されます。




プロジェクトの構成
------------------
:googkit.cfg:  プロジェクトの設定ファイル
:closure/:     ダウンロードした Closure Tools が格納される
:development/: 開発用
:debug/:       デバッグ用(デバッグが有効のときのみ作成される)
:production/:  本番用




ユニットテストを実行する
------------------------
`jsunit 形式 <http://www.infoq.com/jp/articles/javascript-tdd>`_ の
ユニットテストを実行できます。


1. テスト用のHTMLを作成する

   `example_test.html <https://github.com/googkit/googkit/blob/master/template/development/js_dev/example_test.html>`_ を
   テスト対象と同じディレクトリにコピーしてから、名前を
   ``{target_name}_test.html`` に変更します。

   デフォルトの名前 ``{target_name}_test.html`` が気に入らない場合は、
   ``googkit.cfg`` の ``test_file_pattern`` で変更できます。


2. テストコードを書く


3. 設定変更を適用し、依存情報を更新する::

     $ googkit ready


4. テストを実行する

   テスト用のHTMLファイルをブラウザで開きます。

   すべてのテストを実行する場合は、 ``development/all_tests.html`` に
   **http スキーム** でアクセスしてください
   (file スキームではうまくいきません)。




小技
----


コンパイル後のファイル名を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``googkit.cfg`` の ``compiled_js`` を修正します。
編集したあと、以下のコマンドで変更を適用します::

  $ googkit ready


コンパイルしたくないスクリプトがある
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``development/js_dev`` ディレクトリ以外の場所に配置します。
本番用では、このディレクトリ内のファイルはすべてコンパイル・統合されたのち、
削除されてしまいます。


コンパイル後のスクリプトをデバッグする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``--debug`` オプション付きでビルドしてください::

  $ googkit build --debug

``debug/`` ディレクトリが作成され、デバッグ用の機能が使えるようになります。


Source Map を使う
~~~~~~~~~~~~~~~~~
Googkit は、Source Map ファイル ``script.min.js.map`` を ``debug/``
ディレクトリに生成します。
お使いのブラウザが対応していれば、 `Source Map V3 <https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit?pli=1>`_
によるデバッグが可能です。

難読性を保つために、Source Map は ``production/`` ディレクトリには
**保存されません** 。




その他
------


Googkit開発チーム
~~~~~~~~~~~~~~~~~
- cocopon (cocopon@me.com)
- OrgaChem (orga.chem.job@gmail.com)


ライセンス
~~~~~~~~~~
MIT License で配布しています。
詳細は ``LICENSE.txt`` を参照してください。
