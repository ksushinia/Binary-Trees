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
def generate_avl_heights(num_keys, step):
    keys = np.random.permutation(range(1, num_keys + 1))
    root = None
    sizes = []
    heights = []

    for i in range(1, num_keys + 1):
        root = insert(root, keys[i - 1])
        if i % step == 0:  # Сохраняем значения с заданным шагом
            sizes.append(i)
            heights.append(height(root))

    return sizes, heights

# Генерация ключей и построение AVL-дерева (для монотонного роста)
def generate_avl_heights_monotonic(max_keys, step):
    sizes = list(range(step, max_keys + 1, step))
    heights = []

    for size in sizes:
        root = None
        for key in range(1, size + 1):
            root = insert(root, key)
        heights.append(height(root))

    return sizes, heights

# Построение графика и регрессии
def plot_avl_regression():
    max_keys = 100  # Максимальное количество ключей
    step = 5  # Шаг вывода ключей

    # Генерация данных
    sizes_random, heights_random = generate_avl_heights(max_keys, step)
    sizes_monotonic, heights_monotonic = generate_avl_heights_monotonic(max_keys, step)

    # Логарифмическая регрессия для случайных ключей
    log_sizes_random = np.log(sizes_random)
    coefficients_random = np.polyfit(log_sizes_random, heights_random, 1)  # Линейная регрессия на логарифмических данных
    y_pred_random = coefficients_random[0] * log_sizes_random + coefficients_random[1]

    # Логарифмическая регрессия для монотонных ключей
    log_sizes_monotonic = np.log(sizes_monotonic)
    coefficients_mono = np.polyfit(log_sizes_monotonic, heights_monotonic, 1)
    y_pred_mono = coefficients_mono[0] * log_sizes_monotonic + coefficients_mono[1]

    # Теоретическая зависимость O(log n)
    theoretical_heights = [np.log2(n) for n in sizes_monotonic]

    # Вывод регрессионного уравнения
    print(f"Регрессия (случайные ключи): h(N) = {coefficients_random[0]:.6f} * log(N) + {coefficients_random[1]:.6f}")
    print(f"Регрессия (монотонные ключи): h(N) = {coefficients_mono[0]:.6f} * log(N) + {coefficients_mono[1]:.6f}")

    # Построение графиков
    plt.figure(figsize=(10, 6))

    # График для случайных ключей
    plt.scatter(sizes_random, heights_random, color='red', label='Случайные ключи')
    plt.plot(sizes_random, y_pred_random, color='blue', label='Логарифмическая регрессия случайных ключей')

    # График для монотонных ключей
    plt.scatter(sizes_monotonic, heights_monotonic, color='orange', label='Монотонные ключи')
    plt.plot(sizes_monotonic, y_pred_mono, color='purple', label='Логарифмическая регрессия монотонных ключей')

    # Теоретическая кривая
    plt.plot(sizes_monotonic, theoretical_heights, color='green', linestyle='--',
             label='Теоретическая зависимость O(log n)')

    plt.xlabel('Количество ключей')
    plt.ylabel('Высота AVL-дерева')
    plt.title('Зависимость высоты AVL-дерева от количества ключей')
    plt.legend()
    plt.grid(True)
    plt.show()

# Вызов функции построения графика
plot_avl_regression()