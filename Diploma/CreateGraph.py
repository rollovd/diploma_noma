from . import VarshamovGilbertBound, AnalysisHammings, ExtraCapacityCompare
import tqdm
import matplotlib.pylab as plt
from itertools import cycle
plt.style.use('bmh')
color_pal = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

if __name__ == "__main__":
    L = 8
    U = 1000
    delta = 0.6
    n = 256
    p = 0.5

    Q_steps = [1024, 2048, 4096]
    stochastic_values = []
    hamming_values = []
    vg_values = []

    for Q in Q_steps:
        S = Q / L

        vg = VarshamovGilbertBound(L, Q, U, delta, n)
        xaxis, yaxis = vg.get_values(2)

        result_hamming = []
        result_stochastic = []
        users = list(range(1, U, 25))

        for user in tqdm(users):
            value1 = AnalysisHammings(user, S, L).get_r_sigma()
            result_hamming.append(value1)

            value2 = ExtraCapacityCompare(p, Q, L).capacity(user)
            result_stochastic.append(value2)

        hamming_values.append(result_stochastic)
        stochastic_values.append(result_hamming)
        vg_values.append(yaxis)

    colors = ['r', 'b', 'g']
    styles = ['dashed', 'dashdot', 'solid']
    Q_steps = [1024, 2048, 4096]
    # Q_steps =

    plt.figure(figsize=(15, 10))

    for res, color, Q_step in zip(stochastic_values, colors, Q_steps):
        S = int(Q_step / L)
        max_value = "%.1f" % max(res)
        plt.plot(users, res, label=f'Стохастическая матрица (S={S}; R_max={max_value})', color=color,
                 linestyle='dashed')

    for res, color, Q_step in zip(hamming_values, colors, Q_steps):
        S = int(Q_step / L)
        max_value = "%.1f" % max(res)
        plt.plot(users, res, label=f'Веса Хэмминга (S={S}; R_max={max_value})', color=color, linestyle='solid')

    for res, color, Q_step in zip(vg_values, colors, Q_steps):
        S = int(Q_step / L)
        max_value = "%.1f" % max(res)
        plt.plot(xaxis, res, label=f'ВГ (S={S}; R_max={max_value})', color=color, linestyle='dashdot')

    plt.xlabel('U')
    plt.ylabel('R_σ')
    plt.legend()
