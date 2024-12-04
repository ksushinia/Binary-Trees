import random
import matplotlib.pyplot as plt
import numpy as np


class Node:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.NIL = Node(0, 'black')  # NIL-узел (лист)
        self.root = self.NIL

    # Метод для вставки ключа
    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.left = self.NIL
        node.right = self.NIL
        node.color = 'red'  # Новый узел всегда красный
        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None or y == self.NIL:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        self.fix_insert(node)

    # Левый поворот
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Правый поворот
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Метод для балансировки после вставки
    def fix_insert(self, node):
        while node != self.root and node.parent.color == 'red':
            if node.parent == node.parent.parent.left:  # Левое поддерево
                uncle = node.parent.parent.right
                if uncle.color == 'red':
                    uncle.color = 'black'
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.right_rotate(node.parent.parent)
            else:  # Правое поддерево (симметричный случай)
                uncle = node.parent.parent.left
                if uncle.color == 'red':
                    uncle.color = 'black'
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.left_rotate(node.parent.parent)

        self.root.color = 'black'

    def height(self, node):
        if node == self.NIL:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))


# Функция для вставки случайных ключей и записи высот
def generate_random_data():
    tree = RedBlackTree()
    heights = []
    num_keys = list(range(1, 101, 5))

    for n in num_keys:
        key = random.randint(1, 100)  # Генерация случайных ключей
        tree.insert(key)
        heights.append(tree.height(tree.root))

    return num_keys, heights


# Функция для вставки монотонно возрастающих ключей и записи высот
def generate_increasing_data():
    tree = RedBlackTree()
    heights = []
    num_keys = list(range(1, 101, 5))  # Монотонно возрастающие ключи от 1 до 100

    for n in num_keys:
        tree.insert(n)
        heights.append(tree.height(tree.root))

    return num_keys, heights


# Построение регрессионной кривой для случайных данных
def plot_logarithmic_regression(x, y, label):
    log_x = np.log2(x)  # Логарифмирование x по основанию 2
    # Расчёт коэффициентов линейной регрессии по формуле
    A = np.vstack([log_x, np.ones(len(log_x))]).T
    coefficients = np.linalg.lstsq(A, y, rcond=None)[0]  # Решение системы уравнений методом наименьших квадратов

    y_pred = coefficients[0] * log_x + coefficients[1]  # Логарифмическое уравнение

    # Вывод уравнения регрессии в консоль
    print(f"Регрессионное уравнение ({label}): h = {coefficients[0]:.6f} * log2(N) + {coefficients[1]:.6f}")

    return y_pred


# Основной код
keys_random, heights_random = generate_random_data()
keys_increasing, heights_increasing = generate_increasing_data()

# Вычисление регрессии для случайных данных и монотонно возрастающих данных
heights_random_pred = plot_logarithmic_regression(np.array(keys_random), np.array(heights_random), "случайные ключи")
heights_increasing_pred = plot_logarithmic_regression(np.array(keys_increasing), np.array(heights_increasing), "монотонно возрастающие ключи")

# Теоретическая кривая (логарифмическая зависимость)
theoretical_heights = [np.log(n) for n in keys_random]

# Построение графика
plt.figure(figsize=(10, 6))

# Экспериментальные данные для случайных ключей
#plt.scatter(keys_random, heights_random, color='blue', label='Случайные ключи')

# Регрессионная кривая для случайных ключей
plt.plot(keys_random, heights_random_pred, color='red', label='Регрессия (случайные ключи)')

# Экспериментальные данные для монотонно возрастающих ключей
#plt.scatter(keys_increasing, heights_increasing, color='green', label='Монотонно возрастающие ключи')

# Регрессионная кривая для монотонно возрастающих ключей
plt.plot(keys_increasing, heights_increasing_pred, color='orange', label='Регрессия (монотонно возрастающие ключи)')

# Теоретическая кривая
plt.plot(keys_random, theoretical_heights, color='purple', label='Теоретическая кривая O(log n)', linestyle='--')

# Оформление графика
plt.title('Зависимость высоты красно-чёрного дерева от количества ключей')
plt.xlabel('Количество ключей')
plt.ylabel('Высота дерева')
plt.legend()
plt.grid(True)

# Показать график
plt.show()
