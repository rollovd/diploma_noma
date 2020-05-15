import numpy as np
import matplotlib.pylab as plt
from itertools import cycle
plt.style.use('bmh')
color_pal = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

class ExtraCapacityVG:
    def __init__(self, p, Q, L):
        self.p = p
        self.Q = Q
        self.L = L
        self.S = self.Q / self.L

    def capacity_serial_connection_channel(self, t):
        first_addendum = (1 - self.p) ** (t + 1) * np.log2(1 / (1 - self.p))
        second_addendum = (1 - self.p) * (1 - (1 - self.p) ** t) * np.log2(
            (1 - (1 - self.p) ** t) / (1 - (1 - self.p) ** (t + 1)))
        third_addendum = self.p * np.log2(1 / (1 - (1 - self.p) ** (t + 1)))

        result = first_addendum + second_addendum + third_addendum
        return result

    def sum_check(self, u):
        value = 0
        for t in range(1, 100):
            value += pow(u, t) * self.capacity_serial_connection_channel(t) / np.math.factorial(t)

        sum_value = value + self.binary_entropy()
        return sum_value

    def binary_entropy(self):
        result = -self.p * np.log2(self.p) - (1 - self.p) * np.log2(1 - self.p)
        return result

    def capacity(self, u):
        lambda_ = u / self.S
        value = self.Q * lambda_ * np.exp(-lambda_) * self.sum_check(lambda_)
        return value
