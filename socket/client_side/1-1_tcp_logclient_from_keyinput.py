# -*- coding: utf-8 -*-

import socket # ソケットモジュールを取得
import sys # システムモジュールを取得(プログラムの終了シグナル送信に利用)

"""
IPv4,TCPでサーバに接続して、キーボード入力された文字列を送信するクライアントプログラムです.
HOST,PORTに適切な値を設定して実行してください. PORTは講義内で自分が利用すると決めたものを設定してください.
q キーのみが入力されるまで、繰り返しデータを送信します.
実行方法:
 $ python 1-1_tcp_logclient_from_keyinput.py 
"""

HOST = "ccx01.sfc.keio.ac.jp" # 接続先のホスト名(FQDNまたはIPv4)を指定する
PORT = 40000 # ポートを指定する(サーバ側で実行しているコードと合致させる)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCPでソケット接続インスタンスを生成

try:
    client.connect((HOST, PORT)) # ホストとポートを指定し、サーバへ接続要求
except: # 接続できない場合の例外処理
    print("接続できません")
    sys.exit() # 例外時は終了する

while True: #  q キーが押下されるまで、繰り返す
    message = input() # キーボード入力を受け付ける
    if message == "q": # q キーのみが入力された場合は終了
        break
    client.sendall(message.encode("utf-8")) # サーバにテキストを送信

client.close() # ソケット接続を終了