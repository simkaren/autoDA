autoDA
===

ダイマックスアドベンチャーをソロで自動周回するスクリプト.
画像認識を用いて自動で周回し, 色違いを捕獲するたびにLINEで通知を飛ばす.

### 必要なもの

* Arduino + FT232 ([こちら](https://qiita.com/chibi314/items/975784f6e951341fc6ce)の準備を完了したもの)
* キャプチャボード

### PCでの準備(Windows)

Windowsにおける準備を記述します. その他OSについては適当に読み替えてください.

##### ファイルの用意

* gitがインストールされていれば`git clone git@github.com:simkaren/autoDA.git`, されていなければCode→Download ZIPをする.

##### Anacondaの準備

* [Anaconda](https://www.anaconda.com/products/individual-d#download-section)をインストール.
* Anaconda Promptを起動し, 下記コマンドを実行. 途中`[Y/n]`を尋ねられたものにはすべて`Y`と回答.
	```
	conda create -n PokeCon python=3.6
	conda activate PokeCon
	pip install requests
	pip install opencv-python
	pip install pynput
	conda install pyserial
	conda install Pillow
	conda install -c pythonnet pythonnet
	```

##### LINE Notifyの準備

* [LINE Notify](https://notify-bot.line.me/ja/)にログインし, マイページからトークンを発行する.
* `autoDA/notify.py`中の`LINE Notify Token Here`とかかれた部分を, 上記で発行したトークンに書き換える.

### 機器の接続

* Switch--Arduino--FT232--PCのように接続する. このとき, Switch--Arduino側を先に接続する.
* Switch--キャプチャボード--PCのように接続する.

### ゲームの準備

* 戦闘アニメを見ないに設定.
* ダイマックスアドベンチャーを`A`ボタンで開始できるようにする. (研究員の目の前で, 話しかけていない状態)
* Arduinoを接続時に一部ボタン入力が行われるので, 上記の状態に正しくなっているかをきちんと確認する. 

### スクリプトの実行

* Anaconda Promptで必要ならば`conda activate PokeCon`で仮想環境を起動し, `autoDA`ディレクトリまで移動する.
* `python main.py [cameraのID] [FT232のシリアルポート番号]`でスクリプトが実行される.
* cameraのIDやポート番号は, デバイスマネージャー(Windows)などで適当に調べる.
* ゲーム画面が表示され, 動作していればok.

### 細かい設定

##### 行先設定

* `autoDA/command.py`中の`command()`関数中の一行目の変数`ikisaki`を変更することで, 保存している行先の上から何番目を周回するかを変更することができる.

##### ボール設定

* ボールの使用個数を制限することができる. `autoDA/command.py`中の`command()`関数の終盤, `if ball > 800: # ボール消費数チェック`と書かれた部分の数値を調整することで, 適当にボールの使用個数を制限することができる.

##### 画像認識設定

* 画像認識がうまくいかない場合は, 使用しているキャプチャボードの違いによると考えられる. 適当に`camera.isContainTemplate()`メソッドの引数に渡す閾値を調整するか, `autoDA/Templates`中の画像を適当に置き換えることで何とかなる.