import random
import matplotlib.pyplot as plt
import numpy as np  # Для регрессии

# Класс узла бинарного дерева поиска
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# Класс бинарного дерева поиска
class BST:
    def __init__(self):
        self.root = None

    # Вставка ключа в дерево
    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, current, key):
        if key < current.key:
            if current.left is None:
                current.left = Node(key)
            else:
                self._insert_recursive(current.left, key)
        elif key > current.key:
            if current.right is None:
                current.right = Node(key)
            else:
                self._insert_recursive(current.right, key)

    # Метод для вычисления высоты дерева
    def get_height(self):
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node):
        if node is None:
            return 0
        left_height = self._get_height_recursive(node.left)
        right_height = self._get_height_recursive(node.right)
        return 1 + max(left_height, right_height)

# Генерация данных и построение графика зависимости
def analyze_bst():
    num_keys_list = range(1, 101, 5)  # Количество ключей от 1 до 100
    bst = BST()
    heights = []

    keys = random.sample(range(1, 101), 100)  # Генерация 100 случайных ключей
    for i in num_keys_list:
        bst.insert(keys[i - 1])  # Добавляем ключ по одному
        heights.append(bst.get_height())  # Измерение высоты дерева после каждой вставки

    # Построение графика зависимости высоты от количества ключей
    plt.scatter(num_keys_list, heights, color='blue', label='Экспериментальные данные', s=30)

    # Логарифмическая регрессия
    log_keys = np.log(num_keys_list)  # Логарифм от количества ключей
    coefficients = np.polyfit(log_keys, heights, 1)  # Линейная регрессия на логарифмических данных
    regression_line = coefficients[0] * log_keys + coefficients[1]  # Построение регрессии H(n) = a*log(n) + b

    # Вывод уравнения регрессии в консоль
    print(f"Регрессионное уравнение: H(n) = {coefficients[0]:.6f} * log(n) + {coefficients[1]:.6f}")

    # Построение регрессионной кривой
    plt.plot(num_keys_list, regression_line, color='orange', linestyle='--', label='Логарифмическая регрессия')

    # Оформление графика
    plt.title('Зависимость высоты бинарного дерева поиска от количества ключей')
    plt.xlabel('Количество ключей')
    plt.ylabel('Высота дерева')
    plt.legend()  # Легенда для графика
    plt.grid(True)
    plt.show()

# Вызов функции анализа
analyze_bst()
