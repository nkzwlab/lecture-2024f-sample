# -*- coding: utf-8 -*-

import socket # ソケットモジュールを取得

"""
IPv4,TCPでサーバに接続して, 受信データを画面表示するクライアントプログラムです.
HOST,PORTに適切な値を設定して実行してください. PORTは講義内で自分が利用すると決めたものを設定してください.
実行方法:
 $ python 0_tcp_client.py 
"""

HOST =  "ccx01.sfc.keio.ac.jp" # 接続先のホスト名(FQDNまたはIPv4)を指定する
PORT = 9999 # ポートを指定する(サーバ側で実行しているコードと合致させる)
BUFSIZE = 4096 # バッファサイズを指定する

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCPでソケット接続インスタンスを生成

client.connect((HOST, PORT)) # ホストとポートを指定し、サーバへ接続要求

data = client.recv(BUFSIZE) # サーバからデータを受信

print(data.decode("UTF-8")) # 受信データを画面表示

client.close() # ソケット接続を終了