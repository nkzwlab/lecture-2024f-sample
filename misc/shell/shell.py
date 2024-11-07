import subprocess

while True:
    print("$ ", end="")
    cmd = input().split(" ")
    subprocess.run(cmd)
