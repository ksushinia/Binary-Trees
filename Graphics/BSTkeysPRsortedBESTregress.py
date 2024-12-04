import matplotlib.pyplot as plt
import numpy as np

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

# Функция для вставки ключей сбалансированно
def insert_balanced(bst, keys):
    if not keys:
        return
    mid = len(keys) // 2
    bst.insert(keys[mid])
    insert_balanced(bst, keys[:mid])  # Вставка в левое поддерево
    insert_balanced(bst, keys[mid + 1:])  # Вставка в правое поддерево

# Генерация данных и построение графика для лучшего случая
def analyze_best_case_bst():
    num_keys_list = range(1, 101, 5)  # Количество ключей от 1 до 100 с шагом 5
    heights = []

    for i in num_keys_list:
        bst = BST()  # Создаём новое дерево для каждой итерации
        insert_balanced(bst, list(range(1, i + 1)))  # Вставка сбалансированных ключей
        heights.append(bst.get_height())  # Измерение высоты дерева

    # Построение графика зависимости высоты от количества ключей
    plt.scatter(num_keys_list, heights, color='green', label='Экспериментальные данные')

    # Логарифмическая регрессия
    log_keys = np.log(num_keys_list)  # Логарифм количества ключей
    coefs = np.polyfit(log_keys, heights, 1)  # Линейная регрессия на логарифмических данных
    regression_line = coefs[0] * np.log(np.linspace(1, 100, 200)) + coefs[1]

    # Построение регрессионной кривой
    plt.plot(np.linspace(1, 100, 200), regression_line, color='blue', linestyle='--', label='Логарифмическая регрессия')

    # Вывод уравнения регрессии в консоль
    print(f"Регрессионное уравнение: H(n) = {coefs[0]:.6f} * log(n) + {coefs[1]:.6f}")

    # Оформление графика
    plt.title('Зависимость высоты бинарного дерева поиска от количества ключей (лучший случай)')
    plt.xlabel('Количество ключей')
    plt.ylabel('Высота дерева')
    plt.legend()
    plt.grid(True)
    plt.show()

# Вызов функции анализа
analyze_best_case_bst()
