import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

class AVLNode {
    int key, height;
    AVLNode leftChild, rightChild;

    public AVLNode(int key) {
        this.key = key;
        this.height = 1;
    }
}

public class AVLTree {
    AVLNode root;

    // Вставка узла
    public AVLNode insert(AVLNode node, int key) {
        if (node == null) {
            return new AVLNode(key);
        }

        if (key < node.key) {
            node.leftChild = insert(node.leftChild, key);
        } else if (key > node.key) {
            node.rightChild = insert(node.rightChild, key);
        } else {
            System.out.println("Элемент " + key + " уже существует в дереве."); // Если элемент уже есть
            return node; // Не вставляем дубликат
        }

        node.height = 1 + Math.max(height(node.leftChild), height(node.rightChild));
        int balance = getBalance(node);

        // Балансировка
        if (balance > 1 && key < node.leftChild.key) {
            return rightRotate(node);
        }
        if (balance < -1 && key > node.rightChild.key) {
            return leftRotate(node);
        }
        if (balance > 1 && key > node.leftChild.key) {
            node.leftChild = leftRotate(node.leftChild);
            return rightRotate(node);
        }
        if (balance < -1 && key < node.rightChild.key) {
            node.rightChild = rightRotate(node.rightChild);
            return leftRotate(node);
        }

        return node;
    }

    // Поиск узла
    public AVLNode search(AVLNode node, int key) {
        if (node == null || node.key == key) {
            return node;
        }
        if (key < node.key) {
            return search(node.leftChild, key);
        } else {
            return search(node.rightChild, key);
        }
    }

    // Удаление узла
    public AVLNode delete(AVLNode root, int key) {
        if (root == null) {
            System.out.println("Элемент " + key + " не найден в дереве.");
            return root;
        }

        if (key < root.key) {
            root.leftChild = delete(root.leftChild, key);
        } else if (key > root.key) {
            root.rightChild = delete(root.rightChild, key);
        } else {
            if ((root.leftChild == null) || (root.rightChild == null)) {
                AVLNode temp = (root.leftChild != null) ? root.leftChild : root.rightChild;
                if (temp == null) {
                    temp = root;
                    root = null;
                } else {
                    root = temp;
                }
            } else {
                AVLNode temp = minValueNode(root.rightChild);
                root.key = temp.key;
                root.rightChild = delete(root.rightChild, temp.key);
            }
        }

        if (root == null) {
            return root;
        }

        root.height = Math.max(height(root.leftChild), height(root.rightChild)) + 1;
        int balance = getBalance(root);

        if (balance > 1 && getBalance(root.leftChild) >= 0) {
            return rightRotate(root);
        }
        if (balance > 1 && getBalance(root.leftChild) < 0) {
            root.leftChild = leftRotate(root.leftChild);
            return rightRotate(root);
        }
        if (balance < -1 && getBalance(root.rightChild) <= 0) {
            return leftRotate(root);
        }
        if (balance < -1 && getBalance(root.rightChild) > 0) {
            root.rightChild = rightRotate(root.rightChild);
            return leftRotate(root);
        }

        return root;
    }

    // Вспомогательные методы для балансировки
    private int height(AVLNode node) {
        return (node == null) ? 0 : node.height;
    }

    private int getBalance(AVLNode node) {
        return (node == null) ? 0 : height(node.leftChild) - height(node.rightChild);
    }

    private AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.leftChild;
        AVLNode T2 = x.rightChild;
        x.rightChild = y;
        y.leftChild = T2;
        y.height = Math.max(height(y.leftChild), height(y.rightChild)) + 1;
        x.height = Math.max(height(x.leftChild), height(x.rightChild)) + 1;
        return x;
    }

    private AVLNode leftRotate(AVLNode x) {
        AVLNode y = x.rightChild;
        AVLNode T2 = y.leftChild;
        y.leftChild = x;
        x.rightChild = T2;
        x.height = Math.max(height(x.leftChild), height(x.rightChild)) + 1;
        y.height = Math.max(height(y.leftChild), height(y.rightChild)) + 1;
        return y;
    }

    private AVLNode minValueNode(AVLNode node) {
        AVLNode current = node;
        while (current.leftChild != null) {
            current = current.leftChild;
        }
        return current;
    }

    // Обходы дерева
    public void preOrderTraversal(AVLNode node) {
        if (node != null) {
            System.out.print(node.key + " ");
            preOrderTraversal(node.leftChild);
            preOrderTraversal(node.rightChild);
        }
    }

    public void inOrderTraversal(AVLNode node) {
        if (node != null) {
            inOrderTraversal(node.leftChild);
            System.out.print(node.key + " ");
            inOrderTraversal(node.rightChild);
        }
    }

    public void postOrderTraversal(AVLNode node) {
        if (node != null) {
            postOrderTraversal(node.leftChild);
            postOrderTraversal(node.rightChild);
            System.out.print(node.key + " ");
        }
    }

    // Метод для отображения дерева
    public void printTree(AVLNode AVLNode, String indent, boolean last) {
        if (AVLNode != null) {
            System.out.println(indent + (last ? "└── " : "├── ") + AVLNode.key);
            indent += last ? "    " : "│   ";

            printTree(AVLNode.leftChild, indent, false);
            printTree(AVLNode.rightChild, indent, true);
        }
    }



    // Метод обхода в ширину (BFS)
    public void breadthFirstTraversal(AVLNode root) {
        if (root == null) return;
        Queue<AVLNode> queue = new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            AVLNode tempNode = queue.poll();
            System.out.print(tempNode.key + " ");
            if (tempNode.leftChild != null) queue.add(tempNode.leftChild);
            if (tempNode.rightChild != null) queue.add(tempNode.rightChild);
        }
    }
    public boolean isTreeEmpty() {
        return root == null;
    }

    public static void main(String[] args) {
        AVLTree tree = new AVLTree();
        Scanner scanner = new Scanner(System.in);

        int[] array = new int[15];
        for (int i = 0; i < 15; i++) {
            array[i] = i + 1;
        }
        for (int value : array) {
            tree.root = tree.insert(tree.root, value);
        }

        boolean exit = false;
        while (!exit) {
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

            int choice = scanner.nextInt();
            switch (choice) {
                case 1:
                    if (tree.isTreeEmpty()) {
                        System.out.println("Дерево пустое.");
                    } else {
                        tree.printTree(tree.root, "", true);
                    }
                    break;
                case 2:
                    System.out.println("Обход в ширину (BFS):");
                    tree.breadthFirstTraversal(tree.root);
                    System.out.println();
                    break;
                case 3:
                    System.out.println("Прямой обход (Pre-order):");
                    tree.preOrderTraversal(tree.root);
                    System.out.println();
                    break;
                case 4:
                    System.out.println("Симметричный обход (In-order):");
                    tree.inOrderTraversal(tree.root);
                    System.out.println();
                    break;
                case 5:
                    System.out.println("Постфиксный обход (Post-order):");
                    tree.postOrderTraversal(tree.root);
                    System.out.println();
                    break;
                case 6:
                    System.out.print("Введите значение для вставки: ");
                    int valueToInsert = scanner.nextInt();
                    tree.root = tree.insert(tree.root, valueToInsert);
                    System.out.println("Элемент вставлен.");
                    break;
                case 7:
                    System.out.print("Введите значение для поиска: ");
                    int valueToFind = scanner.nextInt();
                    AVLNode result = tree.search(tree.root, valueToFind);
                    if (result != null) {
                        System.out.println("Элемент найден: " + result.key);
                    } else {
                        System.out.println("Элемент не найден.");
                    }
                    break;
                case 8:
                    System.out.print("Введите значение для удаления: ");
                    int valueToDelete = scanner.nextInt();
                    tree.root = tree.delete(tree.root, valueToDelete);
                    System.out.println("Элемент удалён.");
                    break;
                case 9:
                    System.out.println("Выход из программы.");
                    exit = true;
                    break;
                default:
                    System.out.println("Некорректный ввод. Попробуйте снова.");
            }
        }
        scanner.close();
    }
}
