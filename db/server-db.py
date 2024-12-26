# -*- coding: utf-8 -*-

import datetime
import socket
import threading
import time
import sqlite3

"""
IPv4,TCPで接続をうけつけ,クライアントからのメッセージをDBに保存するプログラムです.
リクエストが来ると,新しいスレッドで処理を継続します.
実行方法:
$ python3 server-db.py
"""

PORT = 9999  # ポートを指定

# データベースに接続 (存在しない場合は新規作成)
db_connection = sqlite3.connect("messaging_dev.db")
# カーソルオブジェクトを取得
db_cursor = db_connection.cursor()

server = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # IPv4, TCPでソケット接続インスタンスを生成

server.bind(("", PORT))  # サーバプログラムで使用するポートを紐づける

server.listen()  # 接続待ち状態にする

print("Started server")


# クライアントの要求を処理する関数
def handle_connection(client, address):
    now = datetime.datetime.now()
    print(f"[{now}] 接続要求あり: {address}")  # 接続要求を画面表示

    try:
        # クライアントからのメッセージを受信
        message = client.recv(4096).decode("utf-8")
        print(f"Received message: {message}")

        # 受信したメッセージをDBに書き込み
        db_cursor.execute(
            "INSERT INTO messages (content) VALUES (?)",
            (message,)
        )
        db_connection.commit()

        # クライアントに応答を送信
        response = "Message received! Thank you!\n"
        client.sendall(response.encode("utf-8"))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()  # クライアントからの接続要求を切断


try:
    while True:  # プログラムを実行中は常に以下を実行し続ける
        client, address = server.accept()  # 受信要求用を受け入れてコネクションを確立
        thread = threading.Thread(
            target=handle_connection, args=(client, address)
        )  # 新しいスレッドの作成
        thread.start()  # 作成したスレッドで handle_connection 関数を起動
except KeyboardInterrupt:  # Ctrl + C を押した場合の処理
    print("ソケットを解放します")
    server.close()  # ソケット接続を終了
    db_cursor.close()  # カーソルを閉じる
    db_connection.close()  # DB接続を終了
finally:  # その他の例外発生時の処理
    print("例外発生のため、ソケットを解放します")
    server.close()  # ソケット接続を終了
    db_cursor.close()  # カーソルを閉じる
    db_connection.close()  # DB接続を終了



