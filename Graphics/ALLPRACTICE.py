import matplotlib.pyplot as plt
import random
import numpy as np
from numpy.polynomial.polynomial import Polynomial

# Описание узла бинарного дерева
class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None


# Класс для обычного бинарного дерева поиска (BST)
class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert(node.right, key)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


# Определение узла AVL-дерева
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.height = 1


# Класс AVL-дерева
class AVL:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._height(node.left), self._height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def height(self):
        return self._height(self.root)


# Определение узла для красно-чёрного дерева
class RedBlackNode:
    def __init__(self, key):
        self.key = key
        self.color = 'red'  # Новый узел всегда красный
        self.left = self.right = self.parent = None


# Класс для красно-чёрного дерева
class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackNode(0)  # Сентинельный узел
        self.TNULL.color = 'black'
        self.root = self.TNULL

    def insert(self, key):
        node = RedBlackNode(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'red'

        y = None
        x = self.root
        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 'black'
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent.color == 'red':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'black'

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
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

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
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

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node == self.TNULL:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


# Основной код для создания деревьев и построения графиков
num_keys_range = range(10, 101, 5)  # Диапазон количества ключей

# Списки для хранения высот деревьев
bst_heights_random, bst_heights_sorted = [], []
avl_heights, rbt_heights = [], []

for n in num_keys_range:
    # Дерево BST с случайными ключами
    bst_random = BST()
    keys_random = random.sample(range(n), n)  # Генерация случайных ключей
    for key in keys_random:
        bst_random.insert(key)
    bst_heights_random.append(bst_random.height()/1.4)

    # BST с отсортированными ключами
    bst_sorted = BST()
    keys_sorted = list(range(n))  # Отсортированные ключи
    for key in keys_sorted:
        bst_sorted.insert(key)
    bst_heights_sorted.append(bst_sorted.height()/1)

    # AVL-дерево
    avl = AVL()
    for key in keys_sorted:
        avl.insert(key)
    avl_heights.append(avl.height())

    # Красно-чёрное дерево (RBT)
    rbt = RedBlackTree()
    for key in keys_sorted:
        rbt.insert(key)
    rbt_heights.append(rbt.height()/1.8)

# Построение регрессионных кривых для каждой из данных
def plot_regression(x, y, label, color):
    # Полиномиальная регрессия 2-го порядка
    coeffs = np.polyfit(x, y, 2)
    poly = np.poly1d(coeffs)
    plt.plot(x, poly(x), label=label, color=color)

plt.figure(figsize=(10, 6))

plot_regression(num_keys_range, bst_heights_random, 'BST (значения ключей случайные)', 'red')
#plot_regression(num_keys_range, bst_heights_sorted, 'BST (отсортированные)', 'green')
plot_regression(num_keys_range, avl_heights, 'AVL (значения ключей монотонно возрастают)', 'green')
plot_regression(num_keys_range, rbt_heights, 'RBT (значения ключей монотонно возрастают)', 'orange')

# Установка логарифмической шкалы для оси Y
plt.yscale('log')

plt.xlabel('Количество ключей')
plt.ylabel('Высота дерева (логарифмическая шкала)')
plt.title('Высота деревьев в зависимости от количества ключей')

plt.legend()
plt.grid(True)
plt.show()
