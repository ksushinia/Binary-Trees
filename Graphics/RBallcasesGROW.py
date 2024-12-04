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
            if node.parent == node.parent.parent.left:
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
            else:
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


# Функция для вставки монотонно возрастающих ключей и записи высот
def generate_data():
    tree = RedBlackTree()
    heights = []
    num_keys = list(range(1, 101, 5))  # Монотонно возрастающие ключи от 1 до 100

    for n in num_keys:
        tree.insert(n)
        heights.append(tree.height(tree.root))

    return num_keys, heights


# Генерация данных и построение графика
keys, heights = generate_data()

# Логарифмическая регрессия
log_keys = np.log(keys)
coefficients = np.polyfit(log_keys, heights, 1)  # Логарифмическая регрессия
regression = np.poly1d(coefficients)
heights_pred = regression(log_keys)

# Вывод уравнения регрессии
print(f"Регрессия: h = {coefficients[0]:.6f} * log(N) + {coefficients[1]:.6f}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.scatter(keys, heights, color='blue', label='Экспериментальные данные')
plt.plot(keys, heights_pred, color='red', label='Логарифмическая регрессия')

plt.title('Зависимость высоты красно-чёрного дерева от количества монотонно возрастающих ключей')
plt.xlabel('Количество ключей')
plt.ylabel('Высота дерева')
plt.legend()
plt.grid(True)
plt.show()
