
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import time
import statistics
from matplotlib import animation
from collector import Collector

def dist_mapping( signal ):
    p = -40
    n = 3.7
    result = 10**( ( p - signal ) - (10*n) )
    print(result)
    return result

def plot_mapping( ):

    sigs = list( range(-30, -80, -1) )
    results = list( map( dist_mapping, sigs ) )

    plt.plot(sigs, results)
    plt.show()
    time.sleep(10)
    exit(0)

# TODO try plot mapping function
#plot_mapping()

receiver_list = ['A', 'B', 'C', 'D' , 'E', 'F']
plot_color_map = { 'A': 'r', 'B': 'g', 'C': 'b', 'D': 'r', 'E': 'g', 'F': 'b'  }
plt_map = { 'A' : None, 'B' : None, 'C' : None,  'D' : None, 'E' : None, 'F' : None  }
window = { 'A': [-50, ], 'B': [-50, ], 'C': [-50, ], 'D': [-50, ],  'E': [-50, ],  'F': [-50, ] }
scatter_buffer = { 'A': [[], []], 'B' : [[], []], 'C': [[], []],  'D': [[], []], 'E': [[], []], 'F': [[], []]  } # (time, value)


def animate(args):

    # parse args
    timestamp = args[0]
    data = args[1]
    t = timestamp / 1000.0 # to seconds

    for key in plt_map.keys():
        plt_map[key].clear()
    # dynamically set xlim
    for key in plt_map.keys():
        plt_map[key].set_xlim( t-20.0, t+5.0 )
        plt_map[key].set_ylim(-100, 0)

    # for m in receiver_list: # keep last 100 data
    #     break   # TODO huh?
    #     scatter_buffer[m][0] = scatter_buffer[m][0][-1000:0]
    #     scatter_buffer[m][1] = scatter_buffer[m][1][-1000:0]


    # raw
    # for m in receiver_list:
    #     for point in data['iphone'][m]:
    #         plt_map[m].scatter( t, point, marker='o', color=plot_color_map[m], s=5 )

    # # window average
    window_len = 30
    for m in receiver_list:
        # m = 'A' or 'B' or 'C'
        if m not in data['B001'].keys():
            continue
        for item in data['B001'][m]:  # TODO catch only one
            window[m].append(item)
            if (len(window[m]) > window_len):
                for _ in range(len(window[m]) - window_len):
                    window[m].pop(0)
            scatter_buffer[m][0].append(t)
            scatter_buffer[m][1].append( statistics.mean(window[m]) )

    for m in receiver_list:
        plt_map[m].scatter( scatter_buffer[m][0], scatter_buffer[m][1], color=plot_color_map[m], s=5, )

    # window average-average
    # window_len = 30
    # buffer = { 'A':[], 'B':[], 'C':[],}
    # for m in receiver_list:
    #     # m = 'A' or 'B' or 'C'
    #     for item in data['iphone'][m]:
    #         window[m].append(item)
    #         if (len(window[m]) > window_len):
    #             for _ in range(len(window[m]) - window_len):
    #                 window[m].pop(0)
    #         buffer[m].append( statistics.mean(window[m])  )
    # for m in receiver_list:
    #     plt_map[m].scatter(t, statistics.mean( buffer[m] ), color=plot_color_map[m], s=5, )

def gen_frame_data():
    # generator that never stops
    while True:
        yield c.getQueue()

if __name__ == '__main__':

    fig = plt.figure( figsize= (24,4) )
    plt1 = fig.add_subplot(1, 6, 1)
    plt2 = fig.add_subplot(1, 6, 2)
    plt3 = fig.add_subplot(1, 6, 3)
    plt4 = fig.add_subplot(1, 6, 4)
    plt5 = fig.add_subplot(1, 6, 5)
    plt6 = fig.add_subplot(1, 6, 6)

    # add plt values to pltmap
    plt_map['A'] = plt1
    plt_map['B'] = plt2
    plt_map['C'] = plt3
    plt_map['D'] = plt4
    plt_map['E'] = plt5
    plt_map['F'] = plt6

    c = Collector()
    # while c.getStatus() != 'OK':
    #     print(c.getStatus())
    #     time.sleep(1)

    c.emptyQueue()
    anim = animation.FuncAnimation(fig, animate, frames = gen_frame_data, interval=1000)
    plt.show()