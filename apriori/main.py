#! /usr/bin/python3

import os
import time
import sqlite3
import argparse
import itertools

class Database:
    def __init__(self):
        self.filename = 'database.db'
        self.connect = sqlite3.connect(self.filename)
        self.cursor = self.connect.cursor()
        self.inittable()

    def inittable(self):
        cmds = ["CREATE TABLE origin (id INT, item INT);",
                "CREATE TABLE layer (num INT, itemset text, count INT);"]
        for cmd in cmds:
            self.cursor.execute(cmd)
        self.connect.commit()

    def insert_origin(self, dataid, items):
        cmd = "INSERT INTO origin VALUES (%d, %d);"
        self.cursor.execute(cmd % (dataid, items))

    def insert_layer(self, num, itemset, count):
        cmd = "INSERT INTO layer VALUES (%d, '%s', %d);"
        self.cursor.execute(cmd % (num, itemset, count))

    def do_first_layer(self, minnum):
        cmd = ("SELECT item, a FROM (select item, count(id) as a "
               "FROM origin GROUP BY item) WHERE a >= %s;" % minnum)
        for data in self.cursor.execute(cmd).fetchall():
            self.insert_layer(0, data[0], data[1])
        self.commit()

    def get_layer(self, num):
        cmd = ("SELECT itemset FROM layer WHERE num = %d" % num)
        data = []
        for x in self.cursor.execute(cmd).fetchall():
            data.append(str(x[0]))
        return data

    def get_candicate(self, linenum):
        cmd = ("SELECT item FROM origin WHERE id = %d")
        d = [[] for index in range(linenum)]
        for index in range(linenum):
            for x in self.cursor.execute(cmd % index).fetchall():
                d[index].append(x[0])
        self.candicate = d

    def calc_intersection(self, l):
        cmd = "SELECT id FROM origin WHERE item = %s" % l[0]
        for x in l[1:]:
            cmd = "SELECT id FROM origin WHERE id IN (%s) AND item = %s" % (cmd, x)
        return len(self.cursor.execute(cmd).fetchall())

    def print_layer(self, layer_num):
        cmd = "SELECT count(*) FROM layer WHERE num = %d"
        total = 0
        for i in range(layer_num + 1):
            x = self.cursor.execute(cmd % i).fetchall()[0][0]
            if x != 0:
                total += x
                print('Layer %s: %s itemsets' % (i, x))

        print('Total: %s itemsets' % total)

    def commit(self):
        self.connect.commit()


class Apriori:
    def __init__(self, fname, minsup, minconf, minnum, layerlimit):
        self.tstart = time.time()
        assert minnum or minsup
        self.fname = fname
        if minnum:
            self.minnum = minnum
        else:
            self.minsup = minsup

        self.minconf = minconf

        if layerlimit is None:
            self.layerlimit = 2

        self.db = Database()
        self.loadfilefirst()
        self.execute(1)
        print('Times: %s secs' % (time.time() - self.tstart))

    def loadfilefirst(self):
        self.linenum = 0
        with open(self.fname, 'r') as fout:
            for line in fout:
                for x in map(lambda x: int(x), line.strip().split(', ')):
                    self.db.insert_origin(self.linenum, x)
                self.linenum += 1

        self.db.commit()

        if not hasattr(self, 'minnum'):
            self.minnum = self.minsup * index

        self.db.do_first_layer(self.minnum)
        self.db.get_candicate(self.linenum)

    def execute(self, layer_num):
        def strtuple_to_set(l):
            r = []
            for x in l:
                r.append(set([int(y) for y in x[1:-1].split(', ')]))
            return r

        if layer_num == 1:
            l = []
            check = [{int(x)} for x in self.db.get_layer(layer_num - 1)]
            for x in itertools.combinations(check, 2):
                l.append(x[0] | x[1])

        else:
            l = []
            check = strtuple_to_set(self.db.get_layer(layer_num - 1))
            d = {}
            for x in itertools.combinations(check, layer_num):
                g = x[0] | x[1]
                if len(g) == layer_num + 1:
                    key = tuple(sorted(list(g)))
                    if key not in d:
                        d[key] = 0
                    d[key] += 1

            for key, value in d.items():
                if value == layer_num + 1:
                    l.append(set(key))

        if not l:
            return

        for candi in l:
            count = self.db.calc_intersection(list(candi))
            if count >= self.minnum:
                self.db.insert_layer(layer_num, str(candi), count)

        self.db.commit()
        self.layer_num = layer_num
        self.execute(layer_num + 1)


def main():
    parser = argparse.ArgumentParser(description='Process args')
    parser.add_argument('--file', type=str, help='Input file to parse')
    parser.add_argument('--minsup', type=float, help='Mininum support')
    parser.add_argument('--minconf', type=float, help='Mininum Confidence')
    parser.add_argument('--layerlimit', type=int, help='Limit the layer num')
    parser.add_argument('--minnum', type=int, help='Mininum Number')
    args = parser.parse_args()
    os.system('rm database.db; touch database.db')
    a = Apriori(args.file, args.minsup, args.minconf, args.minnum,
                args.layerlimit)

    a.db.print_layer(a.layer_num)

if __name__ == '__main__':
    main()
