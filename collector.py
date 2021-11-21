import socket
import pickle
import time
from _thread import *
import queue
import requests
import json
import datetime

"""
PARAMETERS
"""
HOST = '0.0.0.0'
PORT = 50007

QUERY_LINK = 'http://server1.jinhoko.com:30006'
DB_NAME = 'sensor'

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
        ins.basetime = time.time()*1000 # in milliseconds
        ins.isTableEmpty = True
        ins.recentQueryTime = 0
        ins.recentQueryTimeInTS = ""

        ins._updateTableStatus()

    def _updateTableStatus(ins):
        # store last query time
        qstr = "select time, value from raw order by time desc limit 1"
        res = requests.get(url=QUERY_LINK + f'/query?db={DB_NAME}&q={qstr}')
        # check json length
        res = json.loads(res.content)
        if 'series' in res['results'][0].keys():
            ins.isTableEmpty = False
        else:
            return

        # if data exists, update recentquerytime
        timestamp = res['results'][0]['series'][0]['values'][0][0]
        timestamp_b = timestamp
        timestamp = timestamp[:-4]
        unixts = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").timestamp()
        ins.recentQueryTime = int(unixts * 1000)  # ns to ms
        ins.recentQueryTimeInTS = timestamp_b

    def getDBStatus(ins):

        response = requests.get(QUERY_LINK + '/ping')
        return response.status_code == 204

    def emptyQueue(ins):

        ins._updateTableStatus()
        if ins.isTableEmpty:
            print('warning : table has no data!')
        return

    def getQueue(ins):

        timeconstraint = ''
        if not ins.isTableEmpty:
            timeconstraint = f"where time > '{ins.recentQueryTimeInTS}'"
        qstr = f"select time,receiver,beacon,value from raw {timeconstraint} order by time asc"
        res = requests.get(url=QUERY_LINK + f'/query?db={DB_NAME}&q={qstr}')
        resdate = res.headers['Date'][5:-4]
        resdate = int(datetime.datetime.strptime(resdate, "%d %b %Y %H:%M:%S").timestamp()*1000)

        # gather data
        orig = json.loads( res.content )

        if 'series' not in orig['results'][0].keys():
            return (resdate, {})
        data = orig['results'][0]['series'][0]['values']
        result_data = {}
        for t,r,b,v in data:
            if b not in result_data.keys():
                result_data[b] = {}
            if r not in result_data[b].keys():
                result_data[b][r] = []
            result_data[b][r].append(v)

        timestamp = int( datetime.datetime.strptime(data[-1][0][:-4], "%Y-%m-%dT%H:%M:%S.%f").timestamp() * 1000 )
        # update time
        ins._updateTableStatus()

        return (timestamp, result_data)
