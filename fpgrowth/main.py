#! /usr/bin/python3
from element import Node, Tree, Database

MINI = 20
result = set()

def iterbranch(node, key=None):
    global result

    # Don't iter if upper to root
    if node.name == 'ROOT':
        return

    node_list = []
    while node.name != 'ROOT':
        node_list.append(node)
        node = node.parent

    for item in node_list:
        result.add(tuple(sorted(key | {item.name})))
        iterbranch(item.parent, key | {item.name})


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
            data_list.append(l)

        # filter out the data less than MINI, and filter data
        count_dict = {k: v for k, v in count_dict.items() if v >= MINI}
        data_list = [list(filter(lambda x: x in count_dict, i)) for i in data_list]

        # Build Tree
        for data in data_list:
            # data.sort(key=lambda x: (count_dict[x]))
            subtree.addsequence(data)

        # Iterator node
        result.add(tuple([nodename]))
        for node in subtree.headtable[nodename]:
            iterbranch(node.parent, key={nodename})

    for i in range(1, 20):
        print(i, len(list(filter(lambda x: len(x) == i, result))))

if __name__ == '__main__':
    d = Database('T10I10N0.1KD1K.data')
    # d = Database('test.txt')
    d.set_minimum(MINI)
    d.loaddb()
    tree = d.buildtree()

    itertree(tree)
