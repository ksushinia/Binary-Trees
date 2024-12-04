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

# Генерация данных и построение графика зависимости
def analyze_bst():
    num_keys_list = range(1, 101)  # Количество ключей от 1 до 100 с шагом 5
    bst = BST()
    heights = []

    # Генерация равномерно распределённых ключей
    keys = list(range(1, 101))  # Ключи от 1 до 100
    for i in num_keys_list:
        bst.insert(keys[i - 1])  # Вставка ключей по одному
        heights.append(bst.get_height())  # Измерение высоты дерева после каждой вставки

    # Построение графика экспериментальных данных по точкам
    plt.scatter(num_keys_list, heights, color='green', label='Экспериментальные данные')

    # Регрессионная кривая (полином 2-й степени)
    coefficients = np.polyfit(num_keys_list, heights, 2)  # Рассчёт коэффициентов полинома
    polynomial = np.poly1d(coefficients)  # Создание полиномиальной функции
    x_range = np.linspace(1, 100, 100)  # Генерация диапазона значений для кривой
    y_pred = polynomial(x_range)  # Вычисление значений по полиному

    # Построение регрессионной кривой
    plt.plot(x_range, y_pred, color='red', label='Регрессионная кривая')

    # Вывод уравнения полинома в консоль
    print(f"Уравнение регрессии: {coefficients[0]:.6f}x^2 + {coefficients[1]:.6f}x + {coefficients[2]:.6f}")

    # Оформление графика
    plt.title('Зависимость высоты бинарного дерева поиска от количества ключей (sorted keys)')
    plt.xlabel('Количество ключей')
    plt.ylabel('Высота дерева')
    plt.legend()
    plt.grid(True)
    plt.show()

# Вызов функции анализа
analyze_bst()
