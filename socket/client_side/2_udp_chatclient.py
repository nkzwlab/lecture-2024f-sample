# -*- coding: utf-8 -*-

import socket # ソケットモジュールを取得
import threading # スレッドモジュールを取得
import sys # システムモジュールを取得(プログラムの終了シグナル送信に利用)

"""
IPv4,UDPでサーバに接続して, キーボード入力された文字列を送信、サーバから受信した文字列を画面表示するクライアントプログラムです.
HOST,PORTに適切な値を設定して実行してください. PORTは講義内で自分が利用すると決めたものを設定してください.
q キーのみが入力されるまで, 繰り返しデータを送信します.
実行方法:
 $ python 2_udp_chatclient.py 
"""

HOST = "ccx01.sfc.keio.ac.jp" # 接続先のホスト名(FQDNまたはIPv4)を指定する
PORT = 50001 # ポートを指定する(サーバ側で実行しているコードと合致させる)
BUFSIZE = 4096 # バッファサイズを指定

def server_handler(client):
    """
    サーバ接続制御関数
    """
    while True: # クライアント接続がある限りループする
        try: # 例外処理を監視
            data = client.recv(BUFSIZE) # サーバからの受信データを取得
            print(data.decode("UTF-8")) # 受信データを画面表示
        except Exception as e: # 例外発生時の処理
            print(f"error: {e}")
            print("chat client exit")
            sys.exit()
    client.close()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDPでソケット接続インスタンスを生成

port = int(input("PORT: ")) or PORT # キーボード入力でPORTを指定

p = threading.Thread(target=server_handler, args=(client, )) # スレッドを生成

p.setDaemon(True) # スレッドを生成

while True: # プログラムが実行中の限りループ
    message = input("メッセージを入力してください: ") # キーボード入力を受け付け
    client.sendto(message.encode("UTF-8"), (HOST, port)) # ポートとホストを指定して、データ送信
    if message == "q": # キーボード入力が q キーのみの場合は処理を終了する
        break
    if not p.is_alive(): # スレッドがない場合は、スレッドを生成
        p.start()

client.close() # ソケット接続を終了
            