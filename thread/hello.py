import threading
t = threading.Thread(target=print, args=("Hello", "World!"))
print("Starting")
t.start()
t.join()
print("Finished")
