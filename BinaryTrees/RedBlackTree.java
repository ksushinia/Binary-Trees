import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

class RBNode {
    int key;
    RBNode leftChild, rightChild, parent;
    boolean isRed; // true - красный, false - черный

    public RBNode(int key) {
        this.key = key;
        this.leftChild = this.rightChild = this.parent = null;
        this.isRed = true; // Новый узел всегда красный
    }
}

class RedBlackTree {
    private RBNode root;
    private RBNode TNULL; // NIL узел (черный лист)

    public RedBlackTree() {
        TNULL = new RBNode(0);
        TNULL.isRed = false; // Листья всегда черные
        root = TNULL;
    }

    // Вставка узла
    // Вставка узла с проверкой на дубликаты
    public void insert(int key) {
        // Проверяем, существует ли уже узел с таким ключом
        if (search(key) != TNULL) {
            System.out.println("Элемент с ключом " + key + " уже существует в дереве.");
            return;
        }

        RBNode newNode = new RBNode(key);
        newNode.leftChild = TNULL;
        newNode.rightChild = TNULL;

        RBNode y = null;
        RBNode x = root;

        while (x != TNULL) { // Поиск места для вставки
            y = x;
            if (newNode.key < x.key) {
                x = x.leftChild;
            } else {
                x = x.rightChild;
            }
        }

        newNode.parent = y;
        if (y == null) {
            root = newNode; // Новый узел становится корнем
        } else if (newNode.key < y.key) {
            y.leftChild = newNode;
        } else {
            y.rightChild = newNode;
        }

        if (newNode.parent == null) {
            newNode.isRed = false; // Корень всегда черный
            return;
        }
        fixInsert(newNode); // Балансировка после вставки
        System.out.println("Элемент с ключом " + key + " успешно вставлен в дерево.");

        fixInsert(newNode); // Балансировка после вставки
    }


    // Балансировка после вставки
    private void fixInsert(RBNode node) {
        while (node.parent != null && node.parent.isRed) {
            if (node.parent == node.parent.parent.leftChild) {
                RBNode uncle = node.parent.parent.rightChild;
                if (uncle.isRed) {
                    node.parent.isRed = false;
                    uncle.isRed = false;
                    node.parent.parent.isRed = true;
                    node = node.parent.parent;
                } else {
                    if (node == node.parent.rightChild) {
                        node = node.parent;
                        rotateLeft(node);
                    }
                    node.parent.isRed = false;
                    node.parent.parent.isRed = true;
                    rotateRight(node.parent.parent);
                }
            } else {
                RBNode uncle = node.parent.parent.leftChild;
                if (uncle.isRed) {
                    node.parent.isRed = false;
                    uncle.isRed = false;
                    node.parent.parent.isRed = true;
                    node = node.parent.parent;
                } else {
                    if (node == node.parent.leftChild) {
                        node = node.parent;
                        rotateRight(node);
                    }
                    node.parent.isRed = false;
                    node.parent.parent.isRed = true;
                    rotateLeft(node.parent.parent);
                }
            }
        }
        root.isRed = false;
    }

    // Левый поворот
    private void rotateLeft(RBNode node) {
        RBNode rightNode = node.rightChild;
        node.rightChild = rightNode.leftChild;
        if (rightNode.leftChild != TNULL) {
            rightNode.leftChild.parent = node;
        }
        rightNode.parent = node.parent;
        if (node.parent == null) {
            root = rightNode;
        } else if (node == node.parent.leftChild) {
            node.parent.leftChild = rightNode;
        } else {
            node.parent.rightChild = rightNode;
        }
        rightNode.leftChild = node;
        node.parent = rightNode;
    }

    // Правый поворот
    private void rotateRight(RBNode node) {
        RBNode leftNode = node.leftChild;
        node.leftChild = leftNode.rightChild;
        if (leftNode.rightChild != TNULL) {
            leftNode.rightChild.parent = node;
        }
        leftNode.parent = node.parent;
        if (node.parent == null) {
            root = leftNode;
        } else if (node == node.parent.rightChild) {
            node.parent.rightChild = leftNode;
        } else {
            node.parent.leftChild = leftNode;
        }
        leftNode.rightChild = node;
        node.parent = leftNode;
    }

    // Поиск элемента
    public RBNode search(int key) {
        return searchHelper(root, key);
    }

    private RBNode searchHelper(RBNode node, int key) {
        if (node == TNULL || key == node.key) {
            return node;
        }
        if (key < node.key) {
            return searchHelper(node.leftChild, key);
        }
        return searchHelper(node.rightChild, key);
    }

    // Удаление узла из дерева
    public void delete(int key) {
        RBNode nodeToDelete = search(key); // Найти узел для удаления
        if (nodeToDelete == TNULL) {
            System.out.println("Элемент не найден в дереве.");
            return;
        }
        deleteNode(nodeToDelete);
        System.out.println("Элемент с ключом " + key + " успешно удален из дерева.");
    }

    // Основная логика удаления узла
    private void deleteNode(RBNode nodeToDelete) {
        RBNode y = nodeToDelete;
        RBNode x;
        boolean yOriginalColor = y.isRed;

        if (nodeToDelete.leftChild == TNULL) {
            x = nodeToDelete.rightChild;
            transplant(nodeToDelete, nodeToDelete.rightChild);
        } else if (nodeToDelete.rightChild == TNULL) {
            x = nodeToDelete.leftChild;
            transplant(nodeToDelete, nodeToDelete.leftChild);
        } else {
            y = minimum(nodeToDelete.rightChild);
            yOriginalColor = y.isRed;
            x = y.rightChild;

            if (y.parent == nodeToDelete) {
                x.parent = y;
            } else {
                transplant(y, y.rightChild);
                y.rightChild = nodeToDelete.rightChild;
                y.rightChild.parent = y;
            }

            transplant(nodeToDelete, y);
            y.leftChild = nodeToDelete.leftChild;
            y.leftChild.parent = y;
            y.isRed = nodeToDelete.isRed;
        }

        if (!yOriginalColor) {
            fixDelete(x); // Балансировка после удаления
        }
    }

    // Замена одного поддерева другим
    private void transplant(RBNode target, RBNode with) {
        if (target.parent == null) {
            root = with;
        } else if (target == target.parent.leftChild) {
            target.parent.leftChild = with;
        } else {
            target.parent.rightChild = with;
        }
        with.parent = target.parent;
    }

    // Поиск минимального узла в поддереве
    private RBNode minimum(RBNode node) {
        while (node.leftChild != TNULL) {
            node = node.leftChild;
        }
        return node;
    }

    // Балансировка после удаления
    private void fixDelete(RBNode node) {
        while (node != root && !node.isRed) {
            if (node == node.parent.leftChild) {
                RBNode sibling = node.parent.rightChild;
                if (sibling.isRed) {
                    sibling.isRed = false;
                    node.parent.isRed = true;
                    rotateLeft(node.parent);
                    sibling = node.parent.rightChild;
                }
                if (!sibling.leftChild.isRed && !sibling.rightChild.isRed) {
                    sibling.isRed = true;
                    node = node.parent;
                } else {
                    if (!sibling.rightChild.isRed) {
                        sibling.leftChild.isRed = false;
                        sibling.isRed = true;
                        rotateRight(sibling);
                        sibling = node.parent.rightChild;
                    }
                    sibling.isRed = node.parent.isRed;
                    node.parent.isRed = false;
                    sibling.rightChild.isRed = false;
                    rotateLeft(node.parent);
                    node = root;
                }
            } else {
                RBNode sibling = node.parent.leftChild;
                if (sibling.isRed) {
                    sibling.isRed = false;
                    node.parent.isRed = true;
                    rotateRight(node.parent);
                    sibling = node.parent.leftChild;
                }
                if (!sibling.rightChild.isRed && !sibling.leftChild.isRed) {
                    sibling.isRed = true;
                    node = node.parent;
                } else {
                    if (!sibling.leftChild.isRed) {
                        sibling.rightChild.isRed = false;
                        sibling.isRed = true;
                        rotateLeft(sibling);
                        sibling = node.parent.leftChild;
                    }
                    sibling.isRed = node.parent.isRed;
                    node.parent.isRed = false;
                    sibling.leftChild.isRed = false;
                    rotateRight(node.parent);
                    node = root;
                }
            }
        }
        node.isRed = false;
    }
    public boolean isTreeEmpty() {
        return root == TNULL;
    }

    // Печать структуры дерева
    public void printTree() {
        printTreeHelper(root, "", true);
    }

    public void printTreeHelper(RBNode node, String indent, boolean last) {
        if (node != TNULL) {
            System.out.println(indent + (last ? "└── " : "├── ") + node.key + (node.isRed ? "(R)" : "(B)"));
            indent += last ? "    " : "│   ";
            printTreeHelper(node.leftChild, indent, false);
            printTreeHelper(node.rightChild, indent, true);
        }
    }

    // Обходы дерева
    public void inorderTraversal(RBNode node) {
        if (node != TNULL) {
            inorderTraversal(node.leftChild);
            System.out.print(node.key + " ");
            inorderTraversal(node.rightChild);
        }
    }

    public void preorderTraversal(RBNode node) {
        if (node != TNULL) {
            System.out.print(node.key + " ");
            preorderTraversal(node.leftChild);
            preorderTraversal(node.rightChild);
        }
    }

    public void postorderTraversal(RBNode node) {
        if (node != TNULL) {
            postorderTraversal(node.leftChild);
            postorderTraversal(node.rightChild);
            System.out.print(node.key + " ");
        }
    }

    public void levelOrderTraversal() {
        if (root == TNULL) return;
        Queue<RBNode> queue = new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            RBNode current = queue.poll();
            System.out.print(current.key + " ");
            if (current.leftChild != TNULL) queue.add(current.leftChild);
            if (current.rightChild != TNULL) queue.add(current.rightChild);
        }
    }

    // Основной метод (меню взаимодействия)
    public static void main(String[] args) {
        RedBlackTree tree = new RedBlackTree();
        Scanner scanner = new Scanner(System.in);
        int choice, key;

        // Заполнение дерева значениями от 1 до 15
        int[] array = new int[15];
        for (int i = 0; i < 15; i++) {
            array[i] = i + 1;
            tree.insert(array[i]); // Вставка элементов в дерево
        }

        while (true) {
            System.out.println("\nМеню:");
            System.out.println("1. Печать дерева");
            System.out.println("2. Обход в ширину (BFS)");
            System.out.println("3. Прямой обход (Pre-order)");
            System.out.println("4. Симметричный обход (In-order)");
            System.out.println("5. Постфиксный обход (Post-order)");
            System.out.println("6. Вставить элемент");
            System.out.println("7. Найти элемент");
            System.out.println("8. Удалить элемент");
            System.out.println("9. Выход");
            System.out.print("Выберите действие: ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    if (tree.isTreeEmpty()) {
                        System.out.println("Дерево пустое.");
                    } else {
                        tree.printTreeHelper(tree.root, "", true);
                    }
                    break;
                case 2:
                    System.out.println("Обход в ширину (BFS):");
                    tree.levelOrderTraversal();
                    System.out.println();
                    break;
                case 3:
                    System.out.println("Прямой обход (Pre-order):");
                    tree.preorderTraversal(tree.root);
                    System.out.println();
                    break;
                case 4:
                    System.out.println("Симметричный обход (In-order):");
                    tree.inorderTraversal(tree.root);
                    System.out.println();
                    break;
                case 5:
                    System.out.println("Постфиксный обход (Post-order):");
                    tree.postorderTraversal(tree.root);
                    System.out.println();
                    break;
                case 6:
                    System.out.print("Введите ключ для вставки: ");
                    key = scanner.nextInt();
                    tree.insert(key);
                    break;
                case 7:
                    System.out.print("Введите ключ для поиска: ");
                    key = scanner.nextInt();
                    RBNode result = tree.search(key);
                    if (result != tree.TNULL) {
                        System.out.println("Элемент найден: " + result.key);
                    } else {
                        System.out.println("Элемент не найден.");
                    }
                    break;
                case 8:
                    System.out.print("Введите ключ для удаления: ");
                    key = scanner.nextInt();
                    tree.delete(key);
                    break;
                case 9:
                    System.out.println("Выход.");
                    scanner.close();
                    return;
                default:
                    System.out.println("Некорректный выбор.");
            }
        }
    }
}

