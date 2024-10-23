# socket編のサンプルコード

# 概要
pythonの組み込みモジュールであるsocketモジュールを使用して, TCP/UDP通信を行うクライアントアプリケーションを作成します.

参考文献: [PythonによるTCP/IPソケットプログラミング](https://www.amazon.co.jp/dp/4274223248)

## ディレクトリ構成
┬ client_side : ソケット接続するクライアントのpythonプログラム. ローカルPC上で実行する  
└ server_side : ソケット接続するクライアントのpythonプログラム. ccx01などのサーバ上で実行する  


## 0.やってみる
HTTPを極簡易化したTCP接続によりサーバから情報を取得するプログラムを作成する.  
┬ [client_side/0_tcp_client.py](client_side/0_tcp_client.py)  
│ 　-> IPv4,TCP接続を行い、サーバから返される文字列を表示するクライアントプログラム  
└ [server_side/0_tcp_server.py](server_side/0_tcp_server.py)  
　　-> IPv4,TCP接続を行い、クライアント側からの接続要求に対して、クライアント側に文字列を返すサーバプログラム  

## 1.TCPログ転送
TCP接続によるユーザの入力またはファイルからサーバにログを転送するクライアント/サーバプログラムを作成する  .
┬ client_side/  
│　　　　[1-1_tcp_logclient_from_keyinput.py](client_side/1-1_tcp_logclient_from_keyinput.py)   
│ 　　　　　-> IPv4,TCP接続を行い、キーボードから入力された文字列をサーバに送信するクライアントプログラム  
│　　　　[1-2_tcp_logclient_from_file.py](client_side/1-2_tcp_logclient_from_file.py)   
│ 　　　　　-> IPv4,TCP接続を行い、ローカルに保存されたファイルの内容をサーバに送信するクライアントプログラム  
│　　　　[1-2_data.txt](client_side/1-2_data.txt)   
│ 　　　　　->  1-2_tcp_logclient_from_file.pyで読み込むファイル   
└ server_side/  
　 　　　　[1_tcp_logserver.py](server_side/1_tcp_logserver.py)   
　 　　　　　-> IPv4,TCP接続を行い、クライアントから送信された文字列をサーバマシンにファイル保存するサーバプログラム   

## 2.UDPチャット 
UDP接続によるユーザの入力またはファイルからサーバにログを転送するクライアント/サーバプログラムを作成する.  
┬ client_side/  
│　　　　[2_udp_chatclient.py](client_side/2_udp_chatclient.py)   
│ 　　　　　-> IPv4,UDP接続を行い、複数のクライアントのキーボードから入力された文字列をサーバに送信し、送信された文字列を表示するクライアントプログラム  
└ server_side/  
　 　　　　[2_udp_chatserver.py](server_side/2_udp_chatserver.py)   
　 　　　　　-> IPv4,UDP接続を行い、クライアントから送信された文字列を画面表示し、接続されたすべてのクライアントに送信するサーバプログラム   
