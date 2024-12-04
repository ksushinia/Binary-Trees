import java.util.Collections;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.util.Random;
import java.util.ArrayList;

class Node {
    int key;
    Node leftChild, rightChild;

    public Node(int key) {
        this.key = key;
        this.leftChild = this.rightChild = null;
    }
}

public class BinaryTree {
    Node root;

    public BinaryTree() {
        this.root = null;
    }

    // Метод для печати дерева
    public void printTree(Node node, String indent, boolean last) {
        if (node != null) {
            System.out.println(indent + (last ? "└── " : "├── ") + node.key);
            indent += last ? "    " : "│   ";

            printTree(node.leftChild, indent, false);
            printTree(node.rightChild, indent, true);
        }
    }

    // Вставка элемента
    public void insert(int key) {
        if (search(key)) {
            System.out.println("Элемент " + key + " уже существует в дереве.");
        } else {
            root = insertRecursive(root, key);
            System.out.println("Элемент " + key + " успешно вставлен в дерево.");
        }
    }

    private Node insertRecursive(Node node, int key) {
        if (node == null) {
            return new Node(key);
        }

        if (key < node.key) {
            node.leftChild = insertRecursive(node.leftChild, key);
        } else if (key > node.key) {
            node.rightChild = insertRecursive(node.rightChild, key);
        }

        return node;
    }

    // Поиск элемента
    public boolean search(int key) {
        return searchRecursive(root, key);
    }

    private boolean searchRecursive(Node node, int key) {
        if (node == null) {
            return false;
        }

        if (key == node.key) {
            return true;
        }

        return key < node.key ? searchRecursive(node.leftChild, key) : searchRecursive(node.rightChild, key);
    }

    // Удаление элемента
    public void delete(int key) {
        if (!search(key)) {
            System.out.println("Элемент " + key + " не найден в дереве.");
        } else {
            root = deleteRecursive(root, key);
            System.out.println("Элемент " + key + " успешно удалён.");

            // Проверка на пустоту дерева
            if (root == null) {
                System.out.println("Дерево пустое.");
            }
        }
    }


    private Node deleteRecursive(Node node, int key) {
        if (node == null) {
            return null;
        }

        if (key < node.key) {
            node.leftChild = deleteRecursive(node.leftChild, key);
        } else if (key > node.key) {
            node.rightChild = deleteRecursive(node.rightChild, key);
        } else {
            // Узел с одним дочерним элементом или без детей
            if (node.leftChild == null) {
                return node.rightChild;
            } else if (node.rightChild == null) {
                return node.leftChild;
            }

            // Узел с двумя детьми: получаем наименьший элемент в правом поддереве
            node.key = minValue(node.rightChild);

            // Удаляем наименьший элемент из правого поддерева
            node.rightChild = deleteRecursive(node.rightChild, node.key);
        }

        return node;
    }

    // Находим минимальное значение в дереве
    private int minValue(Node node) {
        int minValue = node.key;
        while (node.leftChild != null) {
            minValue = node.leftChild.key;
            node = node.leftChild;
        }
        return minValue;
    }

    // Основной метод
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        BinaryTree tree = new BinaryTree();

        ArrayList<Integer> list = new ArrayList<>();
        for (int i = 1; i <= 15; i++) {
            list.add(i);
        }
        Collections.shuffle(list);

        for (int value : list) {
            tree.insert(value);
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

            int choice = scanner.nextInt();
            switch (choice) {
                case 1:
                    tree.printTree(tree.root, "", true);
                    break;
                case 2:
                    System.out.println("Обход в ширину (BFS):");
                    tree.breadthFirstTraversal();
                    break;
                case 3:
                    System.out.println("Прямой обход (Pre-order):");
                    tree.depthFirstPreOrder(tree.root);
                    System.out.println();
                    break;
                case 4:
                    System.out.println("Симметричный обход (In-order):");
                    tree.depthFirstInOrder(tree.root);
                    System.out.println();
                    break;
                case 5:
                    System.out.println("Постфиксный обход (Post-order):");
                    tree.depthFirstPostOrder(tree.root);
                    System.out.println();
                    break;
                case 6:
                    System.out.print("Введите значение для вставки: ");
                    int insertValue = scanner.nextInt();
                    tree.insert(insertValue);
                    break;
                case 7:
                    System.out.print("Введите значение для поиска: ");
                    int searchValue = scanner.nextInt();
                    if (tree.search(searchValue)) {
                        System.out.println("Элемент найден в дереве.");
                    } else {
                        System.out.println("Элемент отсутствует в дереве.");
                    }
                    break;
                case 8:
                    System.out.print("Введите значение для удаления: ");
                    int deleteValue = scanner.nextInt();
                    tree.delete(deleteValue);
                    System.out.println("Элемент удалён.");
                    break;
                case 9:
                    System.out.println("Выход из программы.");
                    scanner.close();
                    return;
                default:
                    System.out.println("Неверный выбор. Попробуйте снова.");
            }
        }
    }

    // BFS обход
    public void breadthFirstTraversal() {
        if (root == null) return;
        Queue<Node> queue = new LinkedList<>();
        queue.add(root);

        while (!queue.isEmpty()) {
            Node currentNode = queue.poll();
            System.out.print(currentNode.key + " ");

            if (currentNode.leftChild != null) queue.add(currentNode.leftChild);
            if (currentNode.rightChild != null) queue.add(currentNode.rightChild);
        }
        System.out.println();
    }

    // Pre-order обход
    public void depthFirstPreOrder(Node node) {
        if (node == null) return;
        System.out.print(node.key + " ");
        depthFirstPreOrder(node.leftChild);
        depthFirstPreOrder(node.rightChild);
    }

    // In-order обход
    public void depthFirstInOrder(Node node) {
        if (node == null) return;
        depthFirstInOrder(node.leftChild);
        System.out.print(node.key + " ");
        depthFirstInOrder(node.rightChild);
    }

    // Post-order обход
    public void depthFirstPostOrder(Node node) {
        if (node == null) return;
        depthFirstPostOrder(node.leftChild);
        depthFirstPostOrder(node.rightChild);
        System.out.print(node.key + " ");
    }
}
