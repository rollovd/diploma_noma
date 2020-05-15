import numpy as np
import matplotlib.pylab as plt
import copy
from itertools import cycle
plt.style.use('bmh')
color_pal = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

class CollisionModel:

    def __init__(self, U, Q, L, p):
        self.U = U
        self.L = L
        self.S = Q / self.L
        self.p = p

    @staticmethod
    def combination(length, w):
        result = 1
        denomination = 1
        while w:
            result *= (length - (w - 1)) / denomination
            denomination += 1
            w -= 1
        return result

    def probability_collision(self, k):
        combination_value = self.combination(self.U - 1, k)
        second_value = (1 / self.S) ** k
        third_value = (1 - 1 / self.S) ** (self.U - 1 - k)

        return combination_value * second_value * third_value

    def first_theorem_kronecker(self, p):
        probability_matrix = np.array([[1-p, p], [0, 1]])

        length = self.L - 1
        static_probability_matrix = copy.deepcopy(probability_matrix)

        for _ in range(length):
            probability_matrix = np.kron(static_probability_matrix, probability_matrix)

        return probability_matrix

    @staticmethod
    def multinomial_coefficient(L, w_list):
        f = lambda x: 0**x or x * f(x - 1)
        r = f(L)
        for i in w_list:
            r //= f(i)
        return r // f(L - sum(w_list))

    def probability_to_transmit_1(self, t):
        return 1 - (1 - self.p) ** t

    def probability_input(self, weight):
        transmit_1 = self.p ** weight
        transmit_0 = (1 - self.p) ** (self.L - weight)

        return transmit_1 * transmit_0

    def probability_output(self, w_stroke):
        probability_output = 0

        for weight in range(w_stroke + 1):
            combination = self.combination(w_stroke, weight)
            value = combination * self.probability_input(weight) * self.probability_supp(w_stroke, weight)
            probability_output += value

        return probability_output

    def probability_supp(self, w_stroke, w):
        if w_stroke <= w:
            return 0

        else:
            probability_sum = 0
            for t in range(self.U):
                prob_collision = self.probability_collision(t)

                transmit_1 = pow(self.p, t * (w_stroke-w))
                transmit_0 = pow(1 - self.p ** t, self.L - w_stroke)

                probability_sum += prob_collision * transmit_1 * transmit_0

            return probability_sum

    @staticmethod
    def factorial(value):
        return np.math.factorial(value)

    def result_capacity(self):
        outer_sum = 0

        for weight in range(self.L + 1):
            inner_sum = 0
            prob_input = self.probability_input(weight)

            for weight_stroke in range(weight, self.L + 1):
                coefficient = self.multinomial_coefficient(self.L, [weight, weight_stroke - weight])
                prob_supp = self.probability_supp(weight_stroke, weight)
                prob_output = self.probability_output(weight_stroke)

                if prob_supp and prob_input:
                    probability = prob_supp * np.log2(prob_supp / prob_output)
                    inner_sum += coefficient * probability

            outer_sum += inner_sum * prob_input

        return outer_sum

if __name__ == "__main__":
    users = np.arange(1, 250, 10)
    capacity_value = lambda user: CollisionModel(user, 1024, 8, 0.5).result_capacity()
    vectorize_capacity = np.vectorize(capacity_value)

    plt.plot(users, vectorize_capacity(users))