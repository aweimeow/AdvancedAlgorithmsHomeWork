#! /usr/bin/python3
from element import Node, Tree, Database
from test import test
import sys

MINI = 2
result = set()

def iterbranch(node, r_list=[], key=None):
    print('Now Input Node: %s' % node.name)
    if node.name == 'ROOT':
        return []

    node_list = []
    while node.name != 'ROOT':
        node_list.append(node)
        node = node.parent

    print('Node List: %s' % list(map(lambda x: x.name, node_list)))

    for item in node_list:
        r_list.append(tuple(sorted(list(key | {item.name}))))
        print('Now append: %s' % str(tuple(sorted(list(key | {item.name})))) )
        iterbranch(item.parent, r_list, key | {item.name})

    return r_list

def itersubtree(tree, key=None):
    result.add(tuple([key]))
    d = {}
    for node in tree.headtable[key]:
        for data in iterbranch(node.parent, r_list=[], key={key}):
            if data not in d:
                d[data] = 0
            d[data] += 1

    d = {k: v for k, v in d.items() if v >= MINI}

    for k in d.keys():
        result.add(k)

def itertree(tree, key=None):
    global result

    # Iter headtable items
    for nodename, nodelist in tree.headtable.items():
        subtree = Tree()

        data_list = []
        count_dict = {}
        for node in nodelist:
            count = node.value
            l = []
            while node.name != 'ROOT':
                l.insert(0, node.name)
                if node.name not in count_dict:
                    count_dict[node.name] = 0
                count_dict[node.name] += count
                node = node.parent

            for i in range(count):
                data_list.append(l)


        # filter out the data less than MINI, and filter data
        count_dict = {k: v for k, v in count_dict.items() if v >= MINI}
        data_list = [list(filter(lambda x: x in count_dict, i)) for i in data_list]

        #print('Count Dict: %s' % count_dict)
        # Build Tree
        for data in data_list:
            temp = data.pop()
            data.sort(key=lambda x: (count_dict[x]), reverse=True)
            data.append(temp)
            #print(data)
            subtree.addsequence(data)

        ### TEST
        for sname, slist in subtree.headtable.items():
            sdata_list = []
            scount_dict = {}
            for node in slist:
                count = node.value
                l = []
                while node.name != 'ROOT':
                    l.insert(0, node.name)
                    if node.name not in scount_dict:
                        scount_dict[node.name] = 0
                    scount_dict[node.name] += count
                    node = node.parent

                for i in range(count):
                    sdata_list.append(l)
            #print('\t%s %s' % (sname, sdata_list))
        ####

        """
        DEBUG LOG
        * 4, 5, 7 topo find bug
        * Tree is 
            * 3
            * 2
                * 7
                    *4
                        *5
                    *5
                * 4
                    *5
        * iterbranch need to count data, but that will be slow
        """
        # result.add(tuple([nodename]))
        if nodename == '5':
            itersubtree(subtree, key=nodename)
        # Iterator node
        # for node in subtree.headtable[nodename]:
        #     iterbranch(node.parent, key={nodename})


if __name__ == '__main__':
    # d = Database('T10I10N0.1KD1K.data')
    d = Database('small.txt')
    d.set_minimum(MINI)
    d.loaddb()
    tree = d.buildtree()

    itertree(tree)

    for i in range(1, 10):
        print(i, len(list(filter(lambda x: len(x) == i, result))))
        #print('\t%s' % list(filter(lambda x: len(x) == i, result)))
