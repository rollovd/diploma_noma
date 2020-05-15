import matplotlib.pylab as plt
from itertools import cycle
import math
plt.style.use('bmh')
color_pal = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

class AnalysisHammings:
    def __init__(self, U, S, L):
        self.U = U  # Число активных пользователей
        self.S = S  # Число независимых каналов
        self.L = L  # Кол-во слотов в независимом канале
        self.Q = self.S * self.L

    @staticmethod
    def combination(length, w):
        result = 1
        denomination = 1
        while w > 0:
            result *= (length - (w - 1)) / denomination
            denomination += 1
            w -= 1
        return result

    def P_prob_k(self, k):
        return self.combination(self.U - 1, k) * (1 / self.S) ** k * (1 - 1 / self.S) ** (self.U - k - 1)

    def P_in(self, w):
        return self.combination(self.L, w) * 2 ** (-self.L)

    def p(self, k):
        return 1 - 2 ** (-k)

    def P(self, w_check, w, k):
        if w_check < w:
            return 0
        else:
            p_k = self.p(k)
            return self.combination(self.L - w, w_check - w) * \
                   p_k ** (w_check - w) * (1 - p_k) ** (self.L - w_check)

    def P_out(self, w_check, k):
        Sum = 0
        for i in range(w_check + 1):
            Sum += self.P(w_check, i, k) * self.P_in(i)
        return Sum

    def min_bandwidth_collision(self, k):
        outer_sum = 0
        minus_sum = 0

        for i in range(self.L + 1):
            P_out = self.P_out(i, k)
            if P_out > 0:
                minus_sum += P_out * math.log2(P_out)

            inner_sum = 0
            for j in range(i, self.L + 1):
                P = self.P(j, i, k)
                if P > 0:
                    inner_sum += P * math.log2(P)
            outer_sum += self.P_in(i) * inner_sum

        return outer_sum - minus_sum

    def band_coll(self):
        Sum = 0
        for i in range(self.U):
            if i == 0:
                Sum += self.P_prob_k(i)
            else:
                Sum += self.P_prob_k(i) * self.min_bandwidth_collision(i)

        return Sum

    def get_bandwidth(self):
        value = self.band_coll() * self.L
        return value

    def get_r_sigma(self):
        value = self.band_coll() * self.U * self.L
        return value