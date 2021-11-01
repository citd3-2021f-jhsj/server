import socket
import pickle
import time
from _thread import *
import queue

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
    '2D' : 'B005'
}

MACHINE_LIST = [ 'A', 'B', 'C' ]
BEACON_LIST = [ 'B001', 'B002', 'B003', 'B004', 'B005']

"""
class Collector
"""
class Collector(object):

    def __new__(cls, *args, **kwargs):
        # singleton setting
        if not hasattr(cls, 'instance'):
            cls.instance = super(Collector, cls).__new__(cls)
        return cls.instance

    def __init__(ins):
        # initialize
        ins.global_queue = queue.Queue()
        ins.status = 'CONNECTING'
        ins.basetime = time.time()*1000 # in milliseconds

        # start new thread
        start_new_thread( receive_main_thread, (ins, ) )

    def getStatus(ins):
        return ins.status

    def emptyQueue(ins):
        with ins.global_queue.mutex:
            ins.global_queue.queue.clear()

    def getQueue(ins):
        data = []
        while ins.global_queue.qsize():
            data.append( ins.global_queue.get() )

        timestamp = int(time.time()*1000 - ins.basetime)

        # initialize base result dict
        result_dict = {}
        for mid in MACHINE_LIST:
            result_dict[mid] = {}
            for bid in BEACON_LIST:
                result_dict[mid][bid] = []

        for m in data:
            mid = chr(64+m[0])
            for tup in m[1]:
                bid = MAC_MAPPING[tup[0]]
                rssi = tup[1]
                result_dict[mid][bid].append( rssi )

        result = ( timestamp, result_dict )

        return result


def thread_main(ins, conn, ip, port):
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
        parsed_data = []
        for idx in range(num_data):
            snippet = data[idx * 16: (idx + 1) * 16]
            mac_unique = str(snippet[1:2].hex()).upper()
            rssi = bytearray(data[7:11])
            rssi.reverse()
            rssi = int(complement(str(rssi.hex())))
            parsed_data.append((mac_unique, rssi))

        # layout : ( mid, [ (mac_unique, rssi), ... ])
        ins.global_queue.put( (machine_id, parsed_data) )


def complement( hexstr ):
    value = int(hexstr, 16)
    if value & (1 << (32 - 1)):
        value -= 1 << 32
    return value


def receive_main_thread(ins): # receive instance

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
            # report connection status
            if num_curr_clients > 0:
                ins.status = 'OK'
            else:
                ins.status = 'CONNECTING'

            # listen
            try:
                conn.listen(1)
                cli, addr = conn.accept()
#               print(f"[INFO] Client connection established - {addr[0]}:{addr[1]}")
                num_curr_clients += 1
                start_new_thread( thread_main, (ins, cli, addr[0], addr[1]) )
            except Exception as e:
                pass

        # shutdown before continue
        conn.close()
        time.sleep(1)
