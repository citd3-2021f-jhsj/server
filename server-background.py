import socket
import pickle
import time
from _thread import *
import queue
import requests
# pip3 install requests

"""
PARAMETERS
"""
HOST = '0.0.0.0'
PORT = 50007

# TODO change often
MAC_MAPPING= {
    '1C' : 'B001',
    '24' : 'B002',
    '2F' : 'B003',
    '27' : 'B004',
    '2D' : 'B005',
}

MACHINE_LIST = [ 'A', 'B', 'C', 'D' ]   # TODO increase when connecting
TARGET_NUM_MACHINE_CONNECTIONS = len(MACHINE_LIST)
BEACON_LIST = [ 'B001', 'B002', 'B003', 'B004', 'B005', ]

global_queue = queue.Queue()

def thread_main(conn, ip, port):
    while True:
        # receive
        data = conn.recv(1024)
        if not data:
#            print("[WARNING] No data received. Terminating thread")
            conn.close()
            return

        # send back
        conn.send(b'ack')

        machine_id = int.from_bytes(data[1016:1020], byteorder='little')
        num_data = int.from_bytes(data[1020:], byteorder='little')
        #print(num_data)
        parsed_data = []
        for idx in range(num_data):
            snippet = data[idx * 16: (idx + 1) * 16]
            mac_unique = str(snippet[1:2].hex()).upper()
            rssi = bytearray(snippet[7:11])
            rssi.reverse()
            rssi = int(complement(str(rssi.hex())))
            parsed_data.append((mac_unique, rssi))

        # layout : ( mid, [ (mac_unique, rssi), ... ])
        global_queue.put( (machine_id, parsed_data) )
        #print(machine_id, parsed_data)


def complement( hexstr ):
    value = int(hexstr, 16)
    if value & (1 << (32 - 1)):
        value -= 1 << 32
    return value


def receive_main_thread(): # receive instance

    while True:
        # try generate socket
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
#            print("[WARNING] Socket not generated. Retrying")
            conn.close()
            time.sleep(1)
            continue
#           print("[INFO] Socket generated. Now binding")

        # bind socket
        try:
            conn.bind( (HOST, PORT) )
        except Exception as e:
#           print("[WARNING] Port binding failure. Retrying")
            conn.close()
            time.sleep(1)
            continue
#       print("[INFO] Bind done. Now accepting")

        # main accept thread
        num_curr_clients = 0

        while True:
            # listen
            try:
                conn.listen(1)
                print("num of currently connected hosts : ", num_curr_clients)
                cli, addr = conn.accept()
#               print(f"[INFO] Client connection established - {addr[0]}:{addr[1]}")
                num_curr_clients += 1
                start_new_thread( thread_main, (cli, addr[0], addr[1]) )

            except Exception as e:
                pass

        # shutdown before continue
        conn.close()
        time.sleep(1)


if __name__ == '__main__':
    # always start receive thread
    print("start receive thread")
    start_new_thread( receive_main_thread, tuple() )
    # ping database
    print("ping database")
    QUERY_LINK = 'http://server1.jinhoko.com:30006'

    response = requests.get( QUERY_LINK+'/ping')
    assert response.status_code == 204, "cannot ping database"

    # connect database and push
    DB_NAME='sensor'
    TABLE_NAME='raw'
    while True:
        data = []
        while global_queue.qsize():
            data.append(global_queue.get())
        if len(data) == 0:
            continue

        # generate query string and query
        qstr = ''
        dup_idx = 0
        for mid, kvs in data:
            for bid, v in kvs:
                # 'raw,beacon=B001,receiver=A,dup=1 value=-1\n'
                qstr += f'{TABLE_NAME},beacon={MAC_MAPPING[bid]},receiver={chr(64+mid)},dup={dup_idx} value={v} \n'
                dup_idx+=1
        #print(qstr)
        # query
        res = requests.post(url=QUERY_LINK+f'/write?db={DB_NAME}',
                            data=qstr,
                            headers={ 'Content-Type': 'application/octet-stream'}
                            )
        #print(res)

