import numpy as np
import matplotlib.pyplot as plt

# Функция для вычисления теоретической высоты AVL-дерева
def theoretical_avl_height(n):
    return 1.1 * np.log2(n)

# Диапазон значений для количества ключей
num_keys_range = range(10, 101, 5)

# Вычисление теоретической высоты для каждого значения n
theoretical_heights = [theoretical_avl_height(n) for n in num_keys_range]

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(num_keys_range, theoretical_heights, label="Теоретическая высота AVL-дерева", color='blue')

# Настройка графика
plt.xlabel('Количество ключей')
plt.ylabel('Высота дерева')
plt.title('Теоретическая зависимость высоты AVL-дерева от количества ключей')
plt.legend()
plt.grid(True)

# Показать график
plt.show()
