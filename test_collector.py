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
        for key in data['A'].keys():
            if key == 'B001':
                print( key, sum(data['A'][key]) / len(data['A'][key]), len(data['A'][key]) )
