#! /usr/bin/python3

import time
import argparse
import itertools


class Apriori:
    def __init__(self, fname, minsup, minconf, minnum, layerlimit):
        assert minnum or minsup
        if minnum:
            self.minnum = minnum
        else:
            self.minsup = minsup

        self.minconf = minconf

        if layerlimit is None:
            self.layerlimit = 2

        self.loadfile(fname)
        self.execute()

    def loadfile(self, fname):
        self.database = {}
        index = 0
        with open(fname, 'r') as f:
            for line in f:
                for x in line.strip().split(', '):
                    x = int(x)
                    if x not in self.database:
                        self.database[x] = set()
                    self.database[x] |= {index}
                index += 1

        if not hasattr(self, 'minnum'):
            self.minnum = self.minsup * index

        self.layer = [{x: len(y) for x, y in self.database.items() if len(y)>=self.minnum}]
        delkey = list(set(self.database.keys()) - set(self.layer[0].keys()))
        for key in delkey:
            del self.database[key]

    def execute(self):
        for index in range(self.layerlimit):
            layer = self.parselayer(self.layer[index], index + 2)
            if not layer:
                break
            else:
                self.layer.append(layer)

    # 2, 3, 3, 3 and 2 input
    def parselayer(self, layer, index):
        def ctable(layer, index):
            if index > 2:
                keys = set()
                for key in layer.keys():
                    for k in key:
                        keys |= {k}
                keys = list(keys)
            else:
                keys = layer.keys()

            l = list(itertools.combinations(keys, index))
            if index > 2:
                for candi in l:
                    for item in itertools.combinations(candi, index - 1):
                        if item not in self.database:
                            l.remove(candi)
                            break

            return l

        next_layer = {}
        for keys in ctable(layer, index):
            self.database[keys] = self.database[keys[0]].copy()
            for key in keys[1:]:
                self.database[keys] &= self.database[key]

            if len(self.database[keys]) < self.minnum:
                del self.database[keys]
            else:
                next_layer[keys] = len(self.database[keys])
        return next_layer

def main():
    parser = argparse.ArgumentParser(description='Process args')
    parser.add_argument('--file', type=str, help='Input file to parse')
    parser.add_argument('--minsup', type=float, help='Mininum support')
    parser.add_argument('--minconf', type=float, help='Mininum Confidence')
    parser.add_argument('--layerlimit', type=int, help='Limit the layer num')
    parser.add_argument('--minnum', type=int, help='Mininum Number')
    args = parser.parse_args()
    tstart = time.time()
    a = Apriori(args.file, args.minsup, args.minconf, args.minnum,
                args.layerlimit)
    tend = time.time()
    total = 0
    for x in range(len(a.layer)):
        print("Layer %s, Len: %s" % (x, len(a.layer[x])))
        total += len(a.layer[x])
    print('Total Count: %s' % total)
    print('Time Cost: %s' % (tend - tstart))

if __name__ == '__main__':
    main()
