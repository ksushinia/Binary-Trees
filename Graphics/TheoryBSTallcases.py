import matplotlib.pyplot as plt
import numpy as np

# Размеры данных (количество ключей)
num_keys_list = np.arange(1, 101)  # От 1 до 1000 ключей

# Теоретические значения для трёх случаев
best_case = np.log2(num_keys_list)                 # Лучший случай: O(log n)
average_case = np.log2(num_keys_list) * 1.5        # Средний случай: Константа для наглядности
worst_case = num_keys_list                         # Худший случай: O(n)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(num_keys_list, best_case, label='Лучший случай O(log n)', color='green')
plt.plot(num_keys_list, average_case, label='Средний случай ~O(log n)', color='blue')
plt.plot(num_keys_list, worst_case, label='Худший случай O(n)', color='red')

# Оформление графика
plt.title('Асимптотическая сложность бинарного дерева поиска')
plt.xlabel('Количество ключей (n)')
plt.ylabel('Сложность операций')
plt.legend()
plt.grid(True)

# Показать график
plt.show()
