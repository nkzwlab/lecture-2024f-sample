# 最終課題

kino-ma が実装した最終課題のサンプルコードです．

送信，受信の機能を実装しました．

クライアントは作っていないので，実行したい時は後述するコマンドを使ってください．

## ファイル

- `main.py` サーバプログラム
- `protocols/` プロトコル定義が入っている

```
./
├── protocols/
│  ├── receive-request.txt
│  ├── receive-response.txt
│  └── send-request.txt
├── main.py
└── README.md
```

## 使い方

サーバの起動：

```bash
python3 main.py
```

`:12345` ポートで送信サーバ， `:12346` ポートで受信サーバが起動します．

### 動作確認

メッセージの送信

```bash
nc 127.0.0.1 12345 < ./protocols/send-request.txt
```

メッセージの受信

```bash
nc 127.0.0.1 12346 < ./protocols/receive-request.txt
```