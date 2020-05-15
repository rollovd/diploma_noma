import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import cycle
plt.style.use('bmh')
color_pal = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

class Capacity:
    def __init__(self):
        pass

    def capacity_serial_connection_channel(self, t, p):
        first_addendum = (1 - p) ** (t + 1) * np.log2(1 / (1 - p))
        second_addendum = (1 - p) * (1 - (1 - p) ** t) * np.log2((1 - (1 - p) ** t) / (1 - (1 - p) ** (t + 1)))
        third_addendum = p * np.log2(1 / (1 - (1 - p) ** (t + 1)))

        result = first_addendum + second_addendum + third_addendum
        return result

    def capacity_channel(self, L, t, probabilities):
        if t == 0:
            return L

        elif t > 0:
            multiply = lambda L, capacity: L * capacity / L

            vectorize_capacity = np.vectorize(self.capacity_serial_connection_channel)
            vectorize_multiply = np.vectorize(multiply)

            capacity = vectorize_multiply(L, vectorize_capacity(t, probabilities))

            return capacity

    def create_capacity_graph(self, L, list_t):
        plt.figure(figsize=(12, 8))

        probabilities = np.arange(1e-15, 1, 1e-3)
        vectorize_capacity = np.vectorize(self.capacity_channel)

        for t in list_t:
            ax = sns.lineplot(y=vectorize_capacity(L, t, probabilities), x=probabilities,
                              label=f't = {t}')

            plt.setp(ax.get_legend().get_texts(), fontsize='22')
            ax.set(xlabel='p', ylabel=r'C($C^t_{L}$)')

if __name__ == "__main__":
    x = Capacity()
    x.create_capacity_graph(8, [1, 2, 3, 4, 5, 10, 15])