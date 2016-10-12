import cv2
import numpy
import random
import argparse

def distance(source, target):
    x = int(source[0]) - target[0]
    y = int(source[1]) - target[1]
    z = int(source[2]) - target[2]
    return (x ** 2 + y ** 2 + z ** 2) ** 0.5

def main(fname, k):
    img = cv2.imread(fname)
    height, width, channels = img.shape
    l = []
    while len(l) < k:
        h = random.randint(0, height - 1)
        w = random.randint(0, width - 1)
        if (w, h) not in l:
            l.append(img[h, w].tolist())

    while True:
        group_map = [numpy.empty((0, 3), numpy.uint8) for x in range(k)]
        for line in img:
            for pixel in line:
                # Get First k point to calc
                mini = l[0]
                minidis = distance(mini, pixel)
                # If some else's distance less than mini, then replace
                for center in l[1:]:
                    dis = distance(center, pixel)
                    if dis < minidis:
                        minidis = dis
                        mini = center
                group_map[l.index(mini)] = numpy.append(group_map[l.index(mini)], numpy.array([pixel]), axis=0)
        break

    print(len(group_map[0]))
    print(group_map[0].mean(axis=0))
    print(len(group_map[1]))
    print(group_map[1].mean(axis=0))
    print(len(group_map[2]))
    print(group_map[2].mean(axis=0))
    #print(len(group_map[0]), len(group_map[1]), len(group_map[2]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='K-means process Image')
    parser.add_argument('--file', type=str, help='Input File')
    parser.add_argument('-k', type=int, help='K values')
    args = parser.parse_args()
    main(args.file, args.k)
