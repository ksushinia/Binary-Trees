import numpy as np
import matplotlib.pyplot as plt
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


# Генерация данных и построение регрессионных кривых
def analyze_bst_and_rbt_avl():
    num_keys_list = np.arange(1, 101)  # Количество ключей от 1 до 100

    # BST: Средний случай (случайные ключи)
    bst_random = BST()
    heights_random = []
    keys_random = random.sample(range(1, 1001), 100)  # 100 случайных ключей
    for i in num_keys_list:
        bst_random.insert(keys_random[i - 1])
        heights_random.append(0.8 * bst_random.get_height())

    # BST: Лучший случай (сбалансированные ключи)
    heights_best = []
    for i in num_keys_list:
        bst_best = BST()
        insert_balanced(bst_best, list(range(1, i + 1)))
        heights_best.append(0.88 * bst_best.get_height())

    # BST: Худший случай (несбалансированное дерево, последовательная вставка)
    heights_worst = np.array(num_keys_list)

    # Логарифмическая регрессия для BST
    # Преобразуем данные, чтобы провести логарифмическую регрессию
    log_num_keys = np.log(num_keys_list)

    # Подгонка логарифмической регрессии для лучшего и среднего случаев
    coeff_best = np.polyfit(log_num_keys, heights_best, 1)
    coeff_random = np.polyfit(log_num_keys, heights_random, 1)

    regression_best = np.polyval(coeff_best, log_num_keys)
    regression_random = np.polyval(coeff_random, log_num_keys)

    # Теоретическая высота AVL и RBT (логарифмическая)
    heights_avl_theoretical = np.log2(num_keys_list)  # AVL
    heights_rbt_theoretical = np.log(num_keys_list)  # RBT

    # Логарифмическая регрессия для теоретических кривых
    coeff_avl = np.polyfit(log_num_keys, heights_avl_theoretical, 1)
    coeff_rbt = np.polyfit(log_num_keys, heights_rbt_theoretical, 1)

    regression_avl = np.polyval(coeff_avl, log_num_keys)
    regression_rbt = np.polyval(coeff_rbt, log_num_keys)

    # Построение графика
    plt.figure(figsize=(12, 8))

    # Регрессия для BST (случайные и сбалансированные данные)
    plt.plot(num_keys_list, regression_best, label='BST: теоретический лучший случай (логарифмическая регрессия)', color='green')
    plt.plot(num_keys_list, regression_random, label='BST: теоретический средний случай (логарифмическая регрессия)', color='blue')

    # Теоретическая кривая для AVL и RBT
    plt.plot(num_keys_list, regression_avl, label='AVL: теоретическая высота (логарифмическая регрессия)',
             color='orange', linestyle='--')
    plt.plot(num_keys_list, regression_rbt, label='RBT: теоретическая высота (логарифмическая регрессия)',
             color='purple', linestyle='--')

    # Оформление графика
    plt.title('Логарифмические регрессионные кривые высоты BST, AVL и RBT')
    plt.xlabel('Количество ключей')
    plt.ylabel('Высота дерева')
    plt.legend()
    plt.grid(True)
    plt.show()


# Вызов функции анализа
analyze_bst_and_rbt_avl()
