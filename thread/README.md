# socket編のサンプルコード

## 概要

`threading` モジュールを利用して、並列プログラミング・非同期処理に入門します。

## ディレクトリ構成

```
./
├── excersise/
│  ├── 1_multithread-sample.py
│  ├── 2_multithread-server.py
│  └── 3_queue.py
│     (4 はサンプルコードを用意していません)
├── tcp/
│  ├── client.py
│  ├── server-sleep.py
│  └── server-thread.py
├── hello.py
└── README.md
```

## 講義編

### 0. hello world

単純な処理を別スレッドで起動するサンプルプログラムです。

```
cd tcp
python3 hello.py
```

出力

```
Starting
Hello World!
Finished
```


### 1. Sleep つき TCP サーバ

ソケット編で作成した TCP サーバに sleep を付加したものです。  
クライアントの接続を受け取った後、指定された秒数 (5秒) 待機してからデータを返信します。

sleep 中は全ての処理が止まってしまうので、同時に二つ以上のリクエストを送ると5秒以上待たされてしまう、効率が悪いサーバです。

```
cd tcp
python3 server-sleep.py
```

起動したサーバに対して、 `client.py` でリクエストを送信します。

このクライアントプログラムは、同時に複数のリクエストを送信します。  
これにより、 sleep　によってリクエストが遅延していく様子を観察できます。

サーバと別のターミナルで：

```
cd tcp
python3 client.py 9998
```

※デフォルトでは ccx01 サーバに接続するようになっています。  
自分のパソコンでサーバを起動した場合は、 `HOST` 変数の中身を `127.0.0.1` にしてください。

出力：

```
$ python3 client.py 9998
Thread #6133952512: received message = hello! this is single-threaded kino-ma server program!!
Thread #6133952512: time taken = 0:00:05.008312
Thread #6117126144: received message = hello! this is single-threaded kino-ma server program!!
Thread #6117126144: time taken = 0:00:10.012361
Thread #6150778880: received message = hello! this is single-threaded kino-ma server program!!
Thread #6150778880: time taken = 0:00:15.016934
Thread #6184431616: received message = hello! this is single-threaded kino-ma server program!!
Thread #6184431616: time taken = 0:00:20.019945
Thread #6167605248: received message = hello! this is single-threaded kino-ma server program!!
Thread #6167605248: time taken = 0:00:25.024121
Main thread: time taken = 0:00:25.024759
```

### 2. マルチスレッド TCP サーバ

`1.` で作成した sleep つきサーバに、マルチスレッド機能を追加したものです。  
別スレッドでリクエストを処理することで、全ての sleep が同時に進行し、待機時間は5秒ちょうどでキープされます。

```
cd tcp
python3 server-thread.py
```

起動したサーバに対して、 `client.py` でリクエストを送信します。

このクライアントプログラムは、同時に複数のリクエストを送信します。  
先ほどとは異なり、遅延が蓄積せず全てのリクエストが5秒で処理されている様子を観察できます。

サーバと別のターミナルで：

```
cd tcp
python3 client.py 9999
```

※デフォルトでは ccx01 サーバに接続するようになっています。  
自分のパソコンでサーバを起動した場合は、 `HOST` 変数の中身を `127.0.0.1` にしてください。

出力：

```
$ python3 client.py 9999
Thread #6119763968: received message = hello! this is multi-threaded kino-ma server program!!
Thread #6119763968: time taken = 0:00:05.006292
Thread #6187069440: received message = hello! this is multi-threaded kino-ma server program!!
Thread #6136590336: received message = hello! this is multi-threaded kino-ma server program!!
Thread #6136590336: time taken = 0:00:05.006729
Thread #6187069440: time taken = 0:00:05.006886
Thread #6170243072: received message = hello! this is multi-threaded kino-ma server program!!
Thread #6170243072: time taken = 0:00:05.007020
Thread #6153416704: received message = hello! this is multi-threaded kino-ma server program!!
Thread #6153416704: time taken = 0:00:05.007212
Main thread: time taken = 0:00:05.007736
```

## 演習編

### 1. シンプルなマルチスレッディング

簡単なスレッド操作を行う演習問題です。

要件：

1. スレッドを三つ生成する
2. スレッドはそれぞれ 1, 2, 3 秒 `time.sleep()` してから終了する
3. スレッド開始時・終了時に何かしら `print` する (e.g., 自分の thread id)
4. 元のスレッドは、全体が終了するまでにかかった時間を表示する

### 2. マルチスレッド＋ソケット

マルチスレッド TCP サーバを作成する演習問題です。

要件：

1. クライアントからのコネクションを受け付ける
2. コネクションを処理するための新しいスレッドを立ち上げる
3. 新しいスレッドの thread id を取得する
4. thread id を含めたレスポンスを返す

### 3. <応用編> スレッド間通信

複数スレッド間でデータを送受信する演習問題です。
講義編で紹介していない要素を使必要があります。

Python の `queue` モジュールを使ってデータを送受信してください

要件：
1. 好きな大きさ $N$ のリスト $L$ に整数を格納する
   - 例: `list(range(N))`
2. スレッドを好きな数 $K$ 個生成し、リストの一部分 $L[i:j]$ を渡す
3. 各スレッド $T_i$ で $\prod_{i=1}^N L_i$ (全ての要素の積) を計算する
    - `[2, 3, 4]` の場合、 $2 \times 3 \times 4 = 24$
4. 各 $T_i$ の出力をさらに掛けて、それを $1,000,000,007$ で割った余りを出力する
5. $N$ や $K$ の値を変えて実行時間を観察する


### 4. <応用編> スレッド間通信＋TCP

複数スレッド間でデータを送受信しながら、かつサーバとの通信も行う演習問題です。  
講義編で紹介していない要素を使いながら、要件に現れていない工夫をいくつか仕込む必要があります。

要件：
1. サーバ： $L[i:j]$ を受け取って $\prod_{𝑖=1}^N L_i$ を返却するマルチスレッドサーバを作成する
2. クライアント：リスト $L$ を作成して $K$ 個の $L[i:j]$ に分割し、それぞれ別のスレッドでサーバに送信する
3. クライアント：レスポンスの総積を $1,000,000,007$ で割って出力する
4. $N$, $K$ の値や実行場所 (自分のパソコン, ccx0..) を変えて実行時間を観察する
