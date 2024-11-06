# socket編のサンプルコード

## 概要

`threading` モジュールを利用して、並列プログラミング・非同期処理に入門します。

## ディレクトリ構成

```
./
├── tcp/
│  ├── client.py
│  ├── server-sleep.py
│  └── server-thread.py
├── hello.py
└── README.md
```

## 0. hello world

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


## 1. Sleep つき TCP サーバ

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

## 2. マルチスレッド TCP サーバ

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
