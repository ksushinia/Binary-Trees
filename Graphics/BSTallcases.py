import matplotlib.pyplot as plt
import numpy as np
import random


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


# Вставка ключей сбалансированно (для лучшего случая)
def insert_balanced(bst, keys):
    if not keys:
        return
    mid = len(keys) // 2
    bst.insert(keys[mid])
    insert_balanced(bst, keys[:mid])
    insert_balanced(bst, keys[mid + 1:])


# Генерация данных и построение графика
def analyze_bst():
    num_keys_list = range(1, 1001, 5)  # Количество ключей от 1 до 100

    # Средний случай: случайные ключи
    bst_random = BST()
    heights_random = []
    keys_random = random.sample(range(1, 1001), 1000)  # Генерация 100 случайных ключей

    for i in num_keys_list:
        bst_random.insert(keys_random[i - 1])
        heights_random.append(bst_random.get_height())

    # Лучший случай: сбалансированные ключи
    heights_best = []
    for i in num_keys_list:
        bst_best = BST()
        insert_balanced(bst_best, list(range(1, i + 1)))
        heights_best.append(bst_best.get_height())

    # Регрессионная кривая для лучшего случая
    coefficients_best = np.polyfit(num_keys_list, heights_best, 2)
    regression_line_best = np.polyval(coefficients_best, num_keys_list)

    # Регрессионная кривая для среднего случая
    coefficients_random = np.polyfit(num_keys_list, heights_random, 2)
    regression_line_random = np.polyval(coefficients_random, num_keys_list)

    # Худший случай: последовательная вставка (несбалансированное дерево)
    heights_worst = np.array(num_keys_list)  # O(n)

    # Построение графиков
    plt.figure(figsize=(10, 6))
    plt.plot(num_keys_list, np.log2(num_keys_list), label='Лучший случай: O(log n)', color='green')
    plt.plot(num_keys_list, heights_worst, label='Худший случай: O(n)', color='red')

    # Добавление регрессионных кривых
    plt.plot(num_keys_list, regression_line_best, color='orange', linestyle='--',
             label='Регрессионная кривая (лучший случай)')
    plt.plot(num_keys_list, regression_line_random, color='brown', linestyle='--',
             label='Регрессионная кривая (средний случай)')

    # Оформление графика
    plt.title('Сравнение высоты BST в разных случаях')
    plt.xlabel('Количество ключей')
    plt.ylabel('Высота дерева')
    plt.legend()
    plt.grid(True)
    plt.show()


# Вызов функции анализа
analyze_bst()
