# -*- coding: utf-8 -*-

import datetime
import socket  # ソケットモジュールを取得
import sys
import threading  # スレッドモジュールを取得

"""
IPv4,TCPでサーバに接続して, 受信データを画面表示するクライアントプログラムです.
計5回の接続を同時に行い,それぞれにかかった時間を表示します.

PORTはコマンドライン引数から指定することもできます.
9998でシングルスレッド版,9999でマルチスレッド版が起動しています.
実行方法:
$ python3 client.py ポート番号(なくてもよい)
"""

HOST = "ccx01.sfc.keio.ac.jp"  # 接続先のホスト名(FQDNまたはIPv4)を指定する

PORT = 9999  # ポートを指定する(サーバ側で実行しているコードと合致させる)
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

BUFSIZE = 4096  # バッファサイズを指定する


# サーバに接続する関数
def connect():
    id = threading.get_ident()

    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # IPv4, TCPでソケット接続インスタンスを生成

    client_start_time = datetime.datetime.now()

    client.connect((HOST, PORT))  # ホストとポートを指定し、サーバへ接続要求
    data = client.recv(BUFSIZE)  # サーバからデータを受信
    print(
        f"Thread #{id}: received message = {data.decode('UTF-8').strip()}"
    )  # 受信データを画面表示. strip() で改行を除去
    client.close()  # ソケット接続を終了

    client_end_time = datetime.datetime.now()
    client_time_taken = client_end_time - client_start_time
    print(f"Thread #{id}: time taken = {client_time_taken}")  # かかった時間を表示


start_time = datetime.datetime.now()

threads = []  # Thread オブジェクトを格納するリスト

# 5個のクライアントスレッドを作成
for i in range(5):
    th = threading.Thread(target=connect)
    th.start()
    threads.append(th)

# 全クライアントスレッドの終了を待機
for th in threads:
    th.join()

end_time = datetime.datetime.now()
time_taken = end_time - start_time
print(f"Main thread: time taken = {time_taken}")  # 合計でかかった時間を表示
