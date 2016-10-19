import cv2
import time
import numpy
import random
import argparse

class kmean:
    def __init__(self, fname, k):
        if fname:
            self.fname = fname
        else:
            raise Exception

        self.k = k if k else 3

        self.process()

    def distance(self, source, target):
        x = int(source[0]) - target[0]
        y = int(source[1]) - target[1]
        z = int(source[2]) - target[2]
        return (x ** 2 + y ** 2 + z ** 2) ** 0.5

    def process(self):
        img = cv2.imread(self.fname)
        height, width, channels = img.shape
        self.center = list()

        # Random Get some color
        while len(self.center) < self.k:
            h = random.randint(0, height - 1)
            w = random.randint(0, width - 1)
            putin = True
            for x in self.center:
                if self.distance(x, img[h, w]) < (200 / self.k):
                    putin = False
                    break
            if putin:
                self.center.append(img[h, w])

        print('Random Choice Color Done')

        counter = []

        c = 0
        while True:
            x = [[] for i in range(self.k)]
            d = {}
            for line in img:
                for pixel in line:
                    if tuple(pixel) in d:
                        x[d[tuple(pixel)]].append(pixel)
                        continue

                    index = 0
                    mindistance = self.distance(pixel, self.center[0])
                    for i in range(1, self.k):
                        distance = self.distance(pixel, self.center[i])
                        if distance < mindistance:
                            mindistance = distance
                            index = i
                        x[index].append(pixel)
                        d[tuple(pixel)] = index

            self.center = [numpy.mean(i, axis=0) for i in x]

            if counter == [len(i) for i in x]:
                break
            else:
                if c >= 10:
                    break
                print('Run Time: %s' % c)
                counter = [len(i) for i in x]
                c += 1
        print('Run While: %s' % c)

        self.center = [center.astype(int) for center in self.center]
        d = {}
        for i in range(self.k):
            for pixel in x[i]:
                d[tuple(pixel)] = self.center[i]

        for h in range(height):
            for w in range(width):
                img[h, w] = d[tuple(img[h, w])]

        cv2.imwrite("%s-out-%s.jpg" % (self.fname.split('.')[0], self.k), img)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='K-means process Image')
    parser.add_argument('--file', type=str, help='Input File')
    parser.add_argument('-k', type=int, help='K values')
    args = parser.parse_args()
    st = time.time()
    k = kmean(args.file, args.k)
    print('Cost: %s' % (time.time() - st))
