import socket
import pickle
import time
from _thread import *
import queue

# MAC_MAPPING= {
#     '1C' : 'B001',
#     '24' : 'B002',
#     '2F' : 'B003',
#     '27' : 'B004',
#     '2D' : 'B005'
# }

"""
PARAMETERS
"""
HOST = '0.0.0.0'
PORT = 50007
NUM_CLIENT_THREADS=1

global_queue = queue.Queue()

def thread_main(conn, ip, port):
    while True:
        # receive
        data = conn.recv(1024)
        if not data:
            print("[WARNING] No data received. Terminating thread")
            conn.close()
            return
        unpickled_data = pickle.loads(data)
        global_queue.put(unpickled_data)

        # send back
        conn.send(b'ack')

def thread_callback():
    pass

def receive_main_thread():

    while True:
        # try generate socket
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print("[WARNING] Socket not generated. Retrying")
            conn.close()
            time.sleep(1)
            continue
        print("[INFO] Socket generated. Now binding")

        # bind socket
        try:
            conn.bind( (HOST, PORT) )
        except Exception as e:
            print("[WARNING] Port binding failure. Retrying")
            conn.close()
            time.sleep(1)
            continue
        #conn.setblocking(False)
        print("[INFO] Bind done. Now accepting")

        # main accept thread
        num_curr_clients = 0
        while True:
            # listen
            try:
                conn.listen(1)
                cli, addr = conn.accept()
                print(f"[INFO] Client connection established - {addr[0]}:{addr[1]}")
                num_curr_clients += 1
                start_new_thread( thread_main, (cli, addr[0], addr[1]) )
            except Exception as e:
                pass

        # shutdown before continue
        conn.close()
        time.sleep(1)

if __name__ == "__main__":

    # seperate queue to receive data
    start_new_thread( receive_main_thread, () )

    # get stream and process
    while True:
        buffer = []
        base_time = time.time()
        while time.time() - base_time < 3 :
            buffer.append( global_queue.get() )
        print(buffer)
        # TODO tmp coding ; average values collected for 3s of beacon 1
        valuemap = [ [], [], [] ]
        for k, d in buffer:
            if k == 'A':
                if '1C' in d.keys():
                    valuemap[0].append(d['1C'])
            if k == 'B':
                if '1C' in d.keys():
                    valuemap[1].append(d['1C'])
            if k == 'C':
                if '1C' in d.keys():
                    valuemap[2].append(d['1C'])

        avgvalue = [ sum(i)/len(i) if len(i) > 0 else -40 for i in valuemap ]
        print(avgvalue)
        # TODO tmp coding end

        #print(buffer)

