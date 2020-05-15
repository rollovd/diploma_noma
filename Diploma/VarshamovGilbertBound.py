import matplotlib.pylab as plt
from itertools import cycle
import numpy as np
import math
plt.style.use('bmh')
color_pal = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

class VarshamovGilbertBound:
    def __init__(self, L, Q, U, delta, n):
        self.L = L
        self.Q = Q
        self.U = U
        self.q = 2 ** self.L
        self.S = self.Q / self.L
        self.delta = delta
        self.n = n

    def P_s(self, qty):
        return 1 - (1 - 1 / self.S) ** (qty - 1)

    @staticmethod
    def combination(length, w):
        result = 1
        denomination = 1
        while w > 0:
            result *= (length - (w - 1)) / denomination
            denomination += 1
            w -= 1
        return result

    def VG(self):
        asymp = -self.delta * math.log(self.delta, self.q) - (1 - self.delta) * math.log(1 - self.delta, self.q) + \
                self.delta * math.log(self.q - 1, self.q)

        return 1 - asymp

    def binom_distrib(self, qty, n):
        Sum = 0
        for i in np.arange(self.delta * n):
            Sum += self.combination(n, i) * pow(self.P_s(qty), i) * pow(1 - self.P_s(qty), n - i)

        return Sum

    def get_values(self, step):
        mas = []
        xaxis = list(range(1, self.U, step))
        for u in tqdm(xaxis):
            value = self.Q * u * self.L * self.VG() * self.binom_distrib(u, self.n) / self.Q
            mas.append(value)

        return xaxis, mas

    def graph(self, n):
        step = 2
        mas = []
        for u in tqdm(range(1, self.U, step)):
            value = self.Q * u * self.L * self.VG() * self.binom_distrib(u, self.n) / self.Q
            mas.append(value)
        r_max = "%.3f" % max(mas)

        plt.figure(figsize=(12, 8))
        plt.plot(list(range(1, self.U, step)), mas, label='(S_VG, R_max) = ' + str((self.S, r_max)))
        plt.legend(loc='lower right')
        plt.grid(True)
