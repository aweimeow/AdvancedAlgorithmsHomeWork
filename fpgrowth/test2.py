import sys

def test(l):
    c = 0
    with open('T10I10N0.1KD1K.txt') as f:
        for line in f:
            data = list(map(int, line.split(',')))
            if sum(map(lambda x: x in data, l)) == len(l):
                print(c, data)
                c += 1
    return c

if __name__ == '__main__':
    l = list(map(int, sys.argv[1:]))
    test(l)
