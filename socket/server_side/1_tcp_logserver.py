# -*- coding: utf-8 -*-

import socket # ソケットモジュールを取得
import datetime # 日時モジュールを取得
import os # ディレクトリ存在確認およびディレクトリ作成のためのモジュールを取得

"""
IPv4,TCPの接続を受け付け, クライアントの接続要求に対して受信データをファイル保存するコードです.
PORTを適切な値(講義内で自分が利用すると決めたもの)を設定して実行してください.
実行方法:
$ python 0_tcp_client.py 
"""

PORT = 40000 # ポートを指定する
BUFSIZE = 4096 # バッファサイズを指定する
LOG_DIR = "./log" # ログ出力ディレクトリを定義

if not os.path.exists(LOG_DIR): # logディレクトリの存在チェック
    print(f"make directory: {LOG_DIR}")
    os.mkdir(LOG_DIR) # logディレクトリを作成する


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCPでソケット接続インスタンスを生成

server.bind(("", PORT)) # サーバプログラムで使用するポートを紐づける

server.listen() # 接続待ち状態にする

try: # 例外を監視
    while True: # プログラムを実行中は常に以下を実行し続ける
        client, address = server.accept() # 受信要求用を受け入れてコネクションを確立
        datetime_now = datetime.datetime.now() # 現在の日時を取得
        file_name = datetime_now.strftime("%m%d%H%M%S%f") + ".txt" # YYYYMMDDHHMISS 形式の文字列に変換
        print(file_name, "接続要求あり") # サーバに保存するファイル名と接続要求を画面表示
        print(client) # 接続元クライアントを表示
        file_out = open(LOG_DIR + "/" + file_name, "wt") # 保存するファイルオブジェクトを生成
        try: # ファイル保存処理の例外発生を監視
            while True: # コネクションが継続している限りループする
                data = client.recv(BUFSIZE) # クライアントからの送信情報を取得
                if not data: # 送信データがない場合はループを抜ける
                    break
                
                print(data.decode("UTF-8")) # 送信内容を画面表示
                print(data.decode("UTF-8"), file=file_out) # 送信内容をファイルに出力
        except Exception as e: # 例外発生時の処理
            print("エラーが発生しました(接続終了)")
            print(f"error: {e}")
        client.close() # クライアントからの接続を終了
        file_out.close() # ファイルを閉じる
except KeyboardInterrupt: # Ctrl + C を押した場合の処理
    print("ソケットを解放します")
    server.close() # ソケット接続を終了
finally : # その他の例外発生時の処理
    print("例外発生のため、ソケットを解放します")
    server.close() # ソケット接続を終了