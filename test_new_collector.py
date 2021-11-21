import time
from collector import Collector

c = Collector()
c.emptyQueue()

while True:
    print(c.getQueue())
    time.sleep(1)