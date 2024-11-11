# 必要なモジュールをインポートする
# import ...


def run(i: int):
    print("Thread [自分のスレッド ID など] started")

    # `i` 秒スリープする

    print("Thread [自分のスレッド ID など] finished")


for i in range(3):
    # `i` 番目のスレッドを作成し、 `run(i)` を実行する

    # `pass` は意味のない文
    # for の後はインデント付きの分がないといけないので `pass` を入れてあります
    pass
