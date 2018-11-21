import math


def sigmoid(x):
    return 1 / (1 + math.exp(-(x-4)))


for i in range(0, 100):
    print sigmoid(i)*40