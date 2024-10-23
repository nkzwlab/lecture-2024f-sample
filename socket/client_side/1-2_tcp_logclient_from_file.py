# -*- coding: utf-8 -*-

import socket # ソケットモジュールを取得
import sys # システムモジュールを取得(プログラムの終了シグナル送信に利用)

"""
IPv4,TCPでサーバに接続して、保存されたファイルの内容を送信するクライアントプログラムです.
HOST,PORTを適切な値を設定して実行してください. PORTは講義内で自分が利用すると決めたものを設定してください
実行方法:
 $ python 1-2_tcp_logclient_from_file.py 
"""

HOST = "ccx01.sfc.keio.ac.jp" # 接続先のホスト名(FQDNまたはIPv4)を指定する
PORT = 40000 # ポートを指定する(サーバ側で実行しているコードと合致させる)

DATAFILE = "1-2_data.txt" # 送信するファイル名を指定する
file_input = open(DATAFILE, "rt", encoding="utf-8") # ファイルを開いてファイルオブジェクトを取得

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCPでソケット接続インスタンスを生成

try:
    client.connect((HOST, PORT)) # ホストとポートを指定し、サーバへ接続要求
except: # 接続できない場合の例外処理
    print("接続できません")
    sys.exit() # 例外時は終了する

message = file_input.read() # ファイルオブジェクトからファイルの内容を取得
client.sendall(message.encode("utf-8")) # サーバにテキストを送信

client.close() # ソケット接続を終了