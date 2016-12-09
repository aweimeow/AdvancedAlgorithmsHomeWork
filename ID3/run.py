#! /usr/bin/python3

import math
import string
from collections import Counter
from graphviz import Digraph

class Node:
    def __init__(self, name):
        self.name = name
        # Here Have all status of name's target
        # Ex. name = Weather, 
        # 2 keys: sunny, rainy, this two key point to different Node
        # keys = answer, value = result or Node
        self.key = set([name])
        self.child = dict()

    def __str__(self):
        return ('Node(name="{name}", child={child})'.format(
                name=self.name, child=self.child))

    def addchild(self, key, nodename):
        # key: answer for this Node Name
        # Node: Pointer to next Node
        node = Node(nodename)
        node.key |= self.key
        self.child[key] = node
        return node

    def addanswer(self, key, answer):
        # answer can be string or Node
        self.child[key] = answer

class ID3:
    def __init__(self, filename):
        self.filename = filename
        self.loadfile()
        self.root = Node(self.findnode(self.data, self.headers))
        self.build(self.root, self.data)
        self.output()

    def build(self, node, datasets):
        for answer in self.answer[node.name]:
            dataset = list(filter(lambda x: x[node.name] == answer, datasets))
            if len(set(map(lambda x: x[self.result_key], dataset))) == 1:
                node.addanswer(answer, dataset[0][self.result_key])
            elif dataset:
                child = node.addchild(
                    answer, self.findnode(dataset, self.headers - node.key)
                )
                self.build(child, dataset)

    def findnode(self, datasets, headers):
        # datasets: filtered datasets
        # headers: possible header list
        d = dict()
        for header in headers:
            result = self.entropy
            for answer in self.answer[header]:
                data = Counter(map(lambda x: x[self.result_key], filter(lambda x: x[header] == answer, datasets))).values()
                result -= sum(data) * self.calc_entropy(data)
            d[header] = result
        print(d)
        return max(d.keys(), key=lambda x: d[x])

    def loadfile(self):
        self.data = []
        with open(self.filename, 'r') as file:
            header = file.readline().strip().split(',')
            self.result_key = header[-1]
            self.headers = set(header[:-1])
            for data in file:
                self.data.append(dict(zip(header, data.strip().split(','))))

        self.entropy = self.calc_entropy(
            Counter(map(lambda x: x[self.result_key], self.data)).values()
        )

        self.answer = {}
        for key in self.headers:
            self.answer[key] = list(set(map(lambda x: x[key], self.data)))

    def calc_entropy(self, data_list):
        # data_list: [1, 2, 3], calculate this entropy
        ret = 0
        total = sum(data_list)
        for data in data_list:
            ret -= (data / total) * math.log((data / total), 2)
        return ret

    def output(self):
        charlist = iter(list(tuple(string.ascii_letters)))
        dot = Digraph(comment='ID3 Homework')
        def recursive(tag, node):
            for label, child in node.child.items():
                nodetag = next(charlist)
                if type(child) == str:
                    dot.node(nodetag, child, shape="plaintext")
                else:
                    dot.node(nodetag, child.name)
                dot.edge(tag, nodetag, label=label)
                if type(child) != str:
                    recursive(nodetag, child)
        tag = next(charlist)
        dot.node(tag, self.root.name)
        recursive(tag, self.root)
        with open('test-output/round-table.gv', 'w') as file:
            file.write(dot.source)
        dot.render('test-output/round-table.gv', view=True)

if __name__ == '__main__':
    id3 = ID3('test4.csv')