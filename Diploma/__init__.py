import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from itertools import cycle
pd.set_option('max_columns', 50)
plt.style.use('bmh')
color_pal = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

__all__ = [
    'plt',
    'pd',
    'np',
    'sns',
    'cycle',
    'color_pal',
    'color_cycle',
]