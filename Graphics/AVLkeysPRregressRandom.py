import numpy as np
import matplotlib.pyplot as plt

# Класс для представления узла AVL-дерева
class Node:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

# Функция для получения высоты узла
def height(node):
    if not node:
        return 0
    return node.height

# Функция для выполнения правого вращения
def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(height(y.left), height(y.right))
    x.height = 1 + max(height(x.left), height(x.right))
    return x

# Функция для выполнения левого вращения
def left_rotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y

# Получение баланса узла
def get_balance(node):
    if not node:
        return 0
    return height(node.left) - height(node.right)

# Функция для вставки ключа в AVL-дерево
def insert(node, key):
    if not node:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    else:
        return node  # Дубликаты не допускаются

    # Обновление высоты текущего узла
    node.height = 1 + max(height(node.left), height(node.right))

    # Получение баланса и выполнение поворотов при необходимости
    balance = get_balance(node)

    # Левый поворот
    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    # Правый поворот
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    # Лево-правый поворот
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    # Право-левый поворот
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

# Генерация случайных ключей и построение AVL-дерева
def generate_avl_heights(num_keys):
    keys = np.random.permutation(range(1, num_keys + 1))  # Случайное перемешивание ключей
    root = None
    heights = []
    for i in range(num_keys):
        root = insert(root, keys[i])
        heights.append(height(root))
    return list(range(1, num_keys + 1)), heights

# Построение графика и логарифмической регрессии
def plot_avl_regression():
    num_keys = 100  # Максимальное количество ключей
    sizes, heights = generate_avl_heights(num_keys)

    # Преобразование размеров в логарифмическую шкалу
    log_sizes = np.log(sizes)

    # Линейная регрессия для логарифмических данных
    coefficients = np.polyfit(log_sizes, heights, 1)  # Степень 1 для линейной зависимости
    regression_line = coefficients[0] * log_sizes + coefficients[1]  # Уравнение регрессии

    # Шаг для отображения точек на графике
    step = 5
    sizes_step = sizes[::step]          # Каждый 5-й ключ
    heights_step = heights[::step]
    regression_step = regression_line[::step]

    # Вывод уравнения регрессии
    print(f"Уравнение регрессии: h(N) = {coefficients[0]:.6f} * log(N) + {coefficients[1]:.6f}")

    # Построение графика
    plt.scatter(sizes_step, heights_step, color='red', label='Экспериментальные данные')
    plt.plot(sizes_step, regression_step, color='blue', label='Логарифмическая регрессия')
    plt.xlabel('Количество ключей')
    plt.ylabel('Высота AVL-дерева')
    plt.title('Зависимость высоты AVL-дерева от количества ключей')
    plt.legend()
    plt.grid(True)
    plt.show()

# Вызов функции построения графика
plot_avl_regression()