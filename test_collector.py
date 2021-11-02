from collector import Collector
import time

if __name__ == '__main__':

    c = Collector()

    while c.getStatus() != 'OK':
        print(c.getStatus())
        time.sleep(1)

    while True:
        c.emptyQueue()
        time.sleep(1)
        timestamp, data = c.getQueue()
        print(data)