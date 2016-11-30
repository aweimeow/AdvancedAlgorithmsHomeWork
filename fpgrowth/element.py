#! /usr/bin/python3

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        # Parent: Previous Node, Child: A hashtable to children
        self.parent = None
        self.child = {}

    def __str__(self):
        return '<Node %s: %s>' % (self.name, self.value)

    def addChild(self, nodename):
        node = Node(nodename, 1)
        self.child[nodename] = node
        node.parent = self
        return node

    def checkChild(self, nodename):
        return nodename in self.child.keys()

    def getChild(self, nodename):
        return self.child[nodename]

    def increase_value(self):
        self.value += 1
        return self.value


class Tree:
    def __init__(self):
        self.root = Node('ROOT', -1)
        self.headtable = {}

    def addsequence(self, namelist):
        head = self.root
        while namelist:
            name = namelist.pop(0)
            if head.checkChild(name):
                head = head.getChild(name)
                head.increase_value()
            else:
                namelist.insert(0, name)
                break

        while namelist:
            name = namelist.pop(0)
            head = head.addChild(name)
            if not name in self.headtable:
                self.headtable[name] = []
            self.headtable[name].append(head)


class Database:
    def __init__(self, filename):
        self.filename = filename

    def set_minimum(self, mini):
        self.mini = mini

    def loadint(self, fout):
        return int.from_bytes(fout.read(4), byteorder='little')

    def loadgarbage(self, fout):
        return int.from_bytes(fout.read(8), byteorder='little')

    def loaddb(self):
        d = {}
        # """
        with open(self.filename, 'r') as fout:
            for line in fout:
                l = line.strip().split(',')
                for e in l:
                    if e not in d:
                        d[e] = 0
                    d[e] += 1
        """
        with open(self.filename, 'rb') as fout:
            byte = self.loadgarbage(fout)
            n = self.loadint(fout)
            while True:
                l = []
                for i in range(n):
                    e = self.loadint(fout)
                    if e not in d:
                        d[e] = 0
                    d[e] += 1
                byte = self.loadgarbage(fout)
                if byte == 0:
                    break
                n = self.loadint(fout)
        """
        self.d = {k:v for k, v in d.items() if v >= self.mini}

    def buildtree(self):
        tree = Tree()
        # """
        with open(self.filename, 'r') as fout:
            for line in fout:
                l = []
                c = line.strip().split(',')
                for e in c:
                    if e in self.d:
                        l.append(e)
                l = sorted(l, key=lambda x: (self.d[x], x), reverse=True)
                tree.addsequence(l)
        """
        with open(self.filename, 'rb') as fout:
            byte = self.loadgarbage(fout)
            n = self.loadint(fout)
            while True:
                l = []
                for i in range(n):
                    e = self.loadint(fout)
                    if e in self.d:
                        l.append(e)
                l = sorted(l, key=lambda x: self.d[x], reverse=True)
                tree.addsequence(l)
                byte = self.loadgarbage(fout)
                if byte == 0:
                    break
                n = self.loadint(fout)
        """
        return tree
