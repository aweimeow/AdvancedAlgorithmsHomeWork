#! /usr/bin/python3

import time
import argparse
import itertools

class Apriori:
    def __init__(self, fname, minsup, minconf, minnum):
        assert minnum or minsup
        self.fname = fname
        if minnum:
            self.minnum = minnum
        else:
            self.minsup = minsup

        self.minconf = minconf
        self.layer = {}
        self.time = []
        self.execute()
        t = 0
        for x in self.layer.keys():
            c = len(self.layer[x])
            print('Layer %s: %s' % (x, c))
            t += c
        print('Total: %s' % t)
        t = 0
        for x in range(len(self.time)):
            t += self.time[x]
        print('Total: %s' % t)

    def load(self, lay):
        """
        n = 1, layer 0, candidate len = 1
        """
        d = {}
        with open(self.fname, 'rb') as fout:
            byte = fout.read(4)
            byte = fout.read(4)
            n = int.from_bytes(fout.read(4), byteorder='little')
            while True:
                l = []
                for i in range(n):
                    l.append(int.from_bytes(fout.read(4), byteorder='little'))
                for x in itertools.combinations(l, lay):
                    if x not in d:
                        d[x] = 0
                    d[x] += 1
                byte = fout.read(4)
                byte = fout.read(4)
                n = int.from_bytes(fout.read(4), byteorder='little')
                if byte == b"":
                    break

        return {k: v for k, v in d.items() if v >= self.minnum}

    def execute(self):
        num = 1
        while True:
            st = time.time()
            l = self.load(num)        
            self.time.append(time.time() - st)
            print('L%s Done: %s' % (num, (time.time() - st)))
            if not l:
                return
            self.layer[num] = l
            num += 1


def main():
    parser = argparse.ArgumentParser(description='Process args')
    parser.add_argument('--file', type=str, help='Input file to parse')
    parser.add_argument('--minsup', type=float, help='Mininum support')
    parser.add_argument('--minconf', type=float, help='Mininum Confidence')
    parser.add_argument('--minnum', type=int, help='Mininum Number')
    args = parser.parse_args()
    a = Apriori(args.file, args.minsup, args.minconf, args.minnum)

if __name__ == '__main__':
    main()
