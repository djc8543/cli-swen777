import threading
import requests
import sys

URL = sys.argv[1]
NUM_THREADS = 5000

def hit(i):
    try:
        r = requests.get(URL, timeout=10)
    except Exception as e:
        print(f"Request {i} failed:", e)

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=hit, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()