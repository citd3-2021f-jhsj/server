import pickle
from collector import Collector
import time


xpos = int(input('xpos: '))
ypos = int(input('ypos: '))

result = input(f"xpos: {xpos} y: {ypos}, right? : ")
if result != 'y':
    print('exiting!')
    exit(0)

assert type(xpos) is int
assert type(ypos) is int

write_interval = 600
c = Collector()

while c.getStatus() != 'OK':
    print(c.getStatus())
    time.sleep(1)

print('recording!')
starttime = time.time()
c.emptyQueue()
time.sleep(write_interval)
datastore = c.getQueue()[1]

print(datastore)

with open(f'data_4_1104/fingerprint_{xpos}_{ypos}.pickle', 'wb') as f:
    pickle.dump( datastore, f )