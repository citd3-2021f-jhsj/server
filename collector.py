import socket
import pickle
import time
from _thread import *
import queue
import requests

"""
PARAMETERS
"""
HOST = '0.0.0.0'
PORT = 50007

QUERY_LINK = 'http://server1.jinhoko.com:30006'

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

        # store last query time

    def getDBStatus(ins):

        response = requests.get(QUERY_LINK + '/ping')
        return response.status_code == 204

    def emptyQueue(ins):

        # update last query time
        pass

    def getQueue(ins):

        # query using basetime
        # update last query time
        # return
        pass

