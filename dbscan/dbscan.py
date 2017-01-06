#! /usr/bin/python3

import time
import argparse
import numpy as np
from scipy import ndimage, misc

D = np.array([(0, 1), (1, 1), (1, 0), (1, -1), 
              (0, -1), (-1, -1), (-1, 0), (-1, 1)])

def distance(x, y):
    """ only accept 3d np-array, contain uint8 type """
    d = 0
    for i in range(3):
        if x[i] < y[i]:
            d += (y[i] - x[i]) ** 2
        else:
            d += (x[i] - y[i]) ** 2

    return d ** 0.5

def run(name, dist):
    s = time.time()
    face = ndimage.imread(name)

    # We dont need RGB
    correct = np.zeros(face.shape[:2], dtype=bool)


    def generate(point):
        # generate candicate list
        candicate = []

        for d in D:
            nxt = point + d
            if 0 <= nxt[0] < face.shape[0] and 0 <= nxt[1] < face.shape[1]:
                if correct[tuple(nxt)] == False:
                    candicate.append(nxt)

        return candicate

    def iteration(now):
        # now: a point for now
        # points: a list store all point in zone

        zone = list()
        candicate = list()
        zone_check = np.zeros(face.shape[:2], dtype=bool)

        zone.append(now)
        correct[tuple(now)] = True
        candicate.extend(generate(now))

        while candicate:
            nxt = candicate.pop()
            if correct[tuple(nxt)] == True:
                continue

            if distance(face[tuple(now)], face[tuple(nxt)]) < dist:
                zone.append(nxt)

                zone_check[tuple(nxt)] = True
                correct[tuple(nxt)] = True

                candicate.extend(generate(nxt))

        return zone

    while correct.all() != True:
        nowlist = np.where(correct == False)
        now = np.array([nowlist[0][0], nowlist[1][0]])

        zone = np.array(iteration(now)).T
        value = face[zone[0], zone[1]].mean(axis=0)
        face[zone[0], zone[1]] = value

    misc.imsave('%s_%d_output.jpg' % (name.split('.')[0], dist), face)
    print('Process done: %s' % (time.time() - s))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dbscan process')
    parser.add_argument('-f', type=str, help='Input file to process')
    parser.add_argument('-d', type=float, help='Points distance to partition')
    args = parser.parse_args()
    run(args.f, args.d)