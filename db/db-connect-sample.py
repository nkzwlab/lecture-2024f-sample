# SQLite3モジュールをインポート
import sqlite3

# データベースに接続 (存在しない場合は新規作成)
conn = sqlite3.connect("messaging_dev.db")

# カーソルオブジェクトを取得
cur = conn.cursor()

# 任意のSQL文を実行（書き込み）
cur.execute("INSERT INTO messages (content) VALUES ('test')")

# トランザクションをコミット
conn.commit()

# 任意のSQL文を実行（読み込み）
cur.execute("SELECT * FROM messages")

# 結果をリストとして格納
rows = cur.fetchall()

# 結果を表示
print(rows)

# 接続を閉じる
cur.close()
conn.close()