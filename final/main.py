import socket
import sqlite3
import threading


# --- 各種定数の定義 ---


# 送信リクエスト用ポート番号の指定
SEND_PORT = 12345
# 受信リクエスト用ポート番号の指定
RECEIVE_PORT = 12346

# 一度に受け取るデータサイズ
BUFSIZE = 4096

# データベースのファイル名
DATABASE_FILE = "mail.db"
# テーブル名
TABLE_NAME = "messages"


# --- サーバを起動する関数 x 2 ---


# 送信用サーバを起動する関数
def start_send_server():
    server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # IPv4, TCPでソケット接続インスタンスを生成

    server.bind(("", SEND_PORT))  # サーバプログラムで使用するポートを紐づける

    server.listen()  # 接続待ち状態にする

    while True:  # プログラムを実行中は常に以下を実行し続ける
        client, address = server.accept()  # 受信要求用を受け入れてコネクションを確立
        print(f"{address=}")  # 接続元のクライアントを表示

        data = read_data(client)
        print(f"{data=}")

        request = parse_send(data)
        print(f"{request=}")
        # => {
        #     "source": "kino-ma",
        #     "destination": "mirai",
        #     "content": "内容が始まる\nhoge",
        # }

        insert_message(request["source"], request["destination"], request["content"])

        # クライアントに何か返信してあげた方が親切
        # client.sendall(b"ok) # など

        client.close()  # クライアントからの接続要求を切断


# 受信用サーバを起動する関数
def start_receive_server():
    server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # IPv4, TCPでソケット接続インスタンスを生成

    server.bind(("", RECEIVE_PORT))  # サーバプログラムで使用するポートを紐づける

    server.listen()  # 接続待ち状態にする

    while True:  # プログラムを実行中は常に以下を実行し続ける
        client, address = server.accept()  # 受信要求用を受け入れてコネクションを確立
        print(f"{address=}")  # 接続元のクライアントを表示

        data = read_data(client)
        print(f"{data=}")

        request = parse_receive(data)
        print(f"{request=}")
        # => {
        #     "destination": "mirai",
        # }

        # DB からメッセージを検索する
        messages = read_messages(request["destination"])
        # 得られたメッセージ一覧を文字列にする
        response = encode_receive_response(messages)

        client.sendall(response.encode())

        client.close()  # クライアントからの接続要求を切断


# --- ソケットでやり取りするデータに関する関数 ---


# クライアントが送ってきたデータをソケットから読み出す関数
def read_data(client_socket):
    data = ""

    while True:
        received_data = client_socket.recv(BUFSIZE)

        if not received_data:  # データを読み終わった場合はループを終了する
            break

        decoded = received_data.decode()
        data += decoded

    return data


# 送信リクエストをパース（解析）する
def parse_send(data: str) -> dict:
    lines = data.split("\n")

    request = {}
    header_end = 0

    for i, line in enumerate(lines):
        # 行が空っぽだったらヘッダが終わるサイン
        # これ以降はメッセージの内容になるので，どこで終わったかを header_end に記録して終了
        if line == "":
            header_end = i
            break

        key, value = line.split(": ")
        key_lower = key.lower()
        request[key_lower] = value
        # header["source"] = "kino-ma"

    # ヘッダが終わった行の次の行からメッセージの内容が始まる
    request["content"] = "\n".join(lines[header_end + 1 :])

    return request


# 送信リクエストをパース（解析）する
def parse_receive(data: str) -> dict:
    lines = data.split("\n")

    request = {}

    for line in lines:
        # 行が空っぽだったらヘッダが終わるサイン
        # 送信と違って，リクエストにはヘッダしか含まれない
        if line == "":
            break

        key, value = line.split(": ")
        key_lower = key.lower()
        # header["source"] = "kino-ma" みたいな感じになる
        request[key_lower] = value

    return request


# メッセージ取得レスポンスを文字列データに変換する関数
def encode_receive_response(messages: list[dict]) -> str:
    blocks = []

    for message in messages:
        headers = []

        cloned_message = message.copy()
        content: str = cloned_message.pop("content")
        content_lines = content.count("\n") + 1

        cloned_message["Content-Lines"] = str(content_lines)

        for key, value in cloned_message.items():
            line = f"{key.title()}: {value}"
            headers.append(line)

        headers.append

        block = "\n".join(headers) + "\n\n" + content
        blocks.append(block)

    encoded = "\n\n".join(blocks)
    print(f"{encoded=}")
    return encoded


# --- データベース操作に関する関数 ---


# データベースファイルを作り，その中にテーブルを作る関数
def setup_db():
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE messages(source, destination, content)")
    except sqlite3.OperationalError:
        print("テーブル 'messages' はすでに存在します． CREATE TABLE をスキップします")

    con.commit()


# データベースにメッセージを追加する関数
def insert_message(source_user: str, destination_user: str, content: str):
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO messages VALUES (?, ?, ?)",
        (source_user, destination_user, content),
    )
    # => "INSERT INTO messages VALUES ("kino-ma", "mirai", "内容が始まる")"
    con.commit()


# データベースからメッセージを取得する関数
# 宛先（destination）で絞り込む
def read_messages(destination_user: str) -> list[dict]:
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    messages = []

    for row in cur.execute(
        "SELECT * FROM messages WHERE destination = ?", (destination_user,)
    ):
        messages.append({"source": row[0], "destination": row[1], "content": row[2]})

    return messages


# --- メイン処理 ---


def main():
    setup_db()

    send_server_thread = threading.Thread(target=start_send_server)
    send_server_thread.start()

    receive_server_thread = threading.Thread(target=start_receive_server)
    receive_server_thread.start()

    send_server_thread.join()
    receive_server_thread.join()


if __name__ == "__main__":
    main()
