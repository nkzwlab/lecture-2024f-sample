# -*- coding: utf-8 -*-

import socket # ソケットモジュールを取得

PORT = 50001 # ポートを指定する
BUFSIZE = 4096 # バッファサイズを指定する

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDPでソケット接続インスタンスを生成

server.bind(("", PORT)) # サーバプログラムで使用するポートを紐づける

client_list = [] # クライアント一覧を生成

try: # 例外を監視
    while True:  # プログラムを実行中は常に以下を実行し続ける
        data, client = server.recvfrom(BUFSIZE) # クライアントからのデータを受信
        if not (client in client_list): # クライアント一覧に接続クライアントがいない場合は一覧にクライアントを追加する
            client_list.append(client)
        if data.decode("UTF-8") == "q": # クライアント側から q のみが送信された場合はクライアント一覧からクライアントを削除
            client_list.remove(client)
        else: # 通常のメッセージ受信時は以下の処理を行う
            message = f'{str(client)}> {data.decode("UTF-8")}' # 表示メッセージを生成
            print(message) # クライアント、受信内容を表示
            for client in client_list: # 接続が確立されているすべてのクライアントに受信したデータを送信
                server.sendto(message.encode("UTF-8"), client)
except KeyboardInterrupt: # Ctrl + C を押した場合の処理
    print("ソケットを解放します")
    server.close() # ソケット接続を終了
finally : # その他の例外発生時の処理
    print("例外発生のため、ソケットを解放します")
    server.close() # ソケット接続を終了