# -*- coding: utf-8 -*-

import socket
import datetime

"""
IPv4,TCPで接続をうけつけ,クライアントからの接続要求に対して,定型的な文字列を送信するサーバプログラムです.
PORTを適切な値(講義内で自分が利用すると決めたもの)を設定して実行してください.
実行方法:
$ python 0_tcp_server.py 
"""

PORT = 9999 # ポートを指定

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCPでソケット接続インスタンスを生成

server.bind(("", PORT)) # サーバプログラムで使用するポートを紐づける

server.listen() # 接続待ち状態にする

try:
    while True: # プログラムを実行中は常に以下を実行し続ける
        client, address = server.accept() # 受信要求用を受け入れてコネクションを確立
        print(str(datetime.datetime.now()), "接続要求あり") # 接続要求を画面表示
        client.sendall(b"hello! this is takito server program!!\n") # 指定した文字列を接続元クライアントに送る
        print(client) # 接続元のクライアントを表示
        client.close() # クライアントからの接続要求を切断
except KeyboardInterrupt: # Ctrl + C を押した場合の処理
    print("ソケットを解放します")
    server.close() # ソケット接続を終了
finally : # その他の例外発生時の処理
    print("例外発生のため、ソケットを解放します")
    server.close() # ソケット接続を終了