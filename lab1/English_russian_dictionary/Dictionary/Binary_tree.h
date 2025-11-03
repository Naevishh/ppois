/**
 * @file Binary_tree.h
 * @author Ященко Александра
 * @brief Заголовочный файл для бинарного дерева.
 * @details Шаблонный класс, предоставляющий функционал дерева.
 */

#ifndef SEM3_L1_PPOIS_BINARY_TREE_H
#define SEM3_L1_PPOIS_BINARY_TREE_H

#include <string>
#include <algorithm>
#include <stdexcept>

/**
 * @class binary_tree
 * @brief Шаблонный класс сбалансированного бинарного дерева поиска.
 * @tparam key_type Тип ключей узлов дерева.
 * @tparam value_type Тип значений, ассоциированных с ключами.
 *
 * @details Класс реализует самобалансирующееся бинарное дерево, которое автоматически
 * поддерживает высоту поддеревьев для обеспечения эффективного поиска, вставки и
 * удаления элементов. Время выполнения операций: O(log n).
 *
 * @see dictionary
 */
template<typename key_type, typename value_type>
class binary_tree{
private:
    /**
     * @struct tree_node
     * @brief Внутренняя структура узла дерева
     * @details Хранит ключ, значение, указатели на потомков и высоту поддерева
     */
    struct tree_node {
        key_type key_t; ///< Ключ узла
        value_type value_t; ///< Значение узла
        tree_node* left_child; ///< Указатель на левого потомка
        tree_node* right_child; ///< Указатель на правого потомка
        int node_height; ///< Высота поддерева с корнем в этом узле(высота поддерева)
        /**
         * @brief Конструктор с заданными ключом и значением.
         * @param key_t_ Ключ узла.
         * @param value_t_ Значение узла.
         */
        tree_node(const key_type& key_t_, const value_type& value_t_)
                : key_t(key_t_), value_t(value_t_),
                  left_child(nullptr), right_child(nullptr), node_height(1) {}

        /**
         * @brief Копирует ключ и значение.
         * @param other Узел, на основе которого инициализируются поля текущего узла.
         */
        void copy_data(const tree_node* other) {
            key_t = other->key_t;
            value_t = other->value_t;
        }
    };

    tree_node* tree_root; ///< Корень дерева

    /**
     * @brief Получение высоты поддерева.
     * @param current Узел для определения высоты.
     * @return Высота поддерева.
     */
    int get_height(tree_node* current) const {
        return current ? current->node_height : 0;
    }

    /**
     * @brief Обновляет высоту поддерева.
     * @param current Узел, чья высота обновляется.
     * @see get_height
     */
    void update_height(tree_node* current) {
        if (current) {
            current->node_height = 1 + std::max(get_height(current->left_child), get_height(current->right_child));
        }
    }

    /**
     * @brief Получение разницы высот поддеревьев дочерних узлов.
     * @param current Узел для получения разности.
     * @return Разница высот.
     * @see get_height
     */
    int get_balance_factor(tree_node* current) {
        return current ? get_height(current->left_child) - get_height(current->right_child) : 0;
    }

    /**
     * @brief Выполняет правый поворот вокруг узла.
     * @param pivot_node Узел для выполнения поворота.
     * @details Выполняет поворот вокруг узла, в результате которого вместо текущего узла корнем поддерева
     *          становится его левый потомок.
     * @return Указатель на узел, ставший новым корнем текущего поддерева.
     */
    tree_node* right_rotate(tree_node* pivot_node) {
        tree_node *left_child = pivot_node->left_child;
        tree_node *right_subtree = left_child->right_child;

        left_child->right_child = pivot_node;
        pivot_node->left_child = right_subtree;

        update_height(pivot_node);
        update_height(left_child);

        return left_child;
    }

    /**
     * * @brief Выполняет левый поворот.
     * @param pivot_node Узел для выполнения поворота.
     * @details Выполняет поворот вокруг узла, в результате которого вместо текущего узла корнем поддерева
     *          становится его правый потомок.
     * @return Указатель на узел, ставший новым корнем текущего поддерева.
     */
    tree_node* left_rotate(tree_node* pivot_node) {
        tree_node *right_child = pivot_node->right_child;
        tree_node *left_subtree = right_child->left_child;

        right_child->left_child = pivot_node;
        pivot_node->right_child = left_subtree;

        update_height(pivot_node);
        update_height(right_child);

        return right_child;
    }

    /**
     * @brief Выполняет балансировку поддерева.
     * @param current Корень текущего поддерева.
     * @details Выполняет балансировку узла путем поворотов, если коэффициент баланса
     *          превышает допустимые значения. Поддерживает четыре случая нарушения баланса:
     *          левый-левый, правый-правый, левый-правый и правый-левый.
     * @return Корень текущего поддерева.
     */
    tree_node* balance(tree_node* current) {
        update_height(current);
        int balance_factor = get_balance_factor(current);
        if (balance_factor > 1 && get_balance_factor(current->left_child) >= 0)
            return right_rotate(current);
        if (balance_factor < -1 && get_balance_factor(current->right_child) <= 0)
            return left_rotate(current);
        if (balance_factor > 1 && get_balance_factor(current->left_child) < 0) {
            current->left_child = left_rotate(current->left_child);
            return right_rotate(current);
        }
        if (balance_factor < -1 && get_balance_factor(current->right_child) > 0) {
            current->right_child = right_rotate(current->right_child);
            return left_rotate(current);
        }
        return current;
    }

    /**
     * @brief Проверяет равенство двух деревьев.
     * @param tree_node1 Корень первого дерева.
     * @param tree_node2 Корень второго дерева.
     * @return True, если деревья равны, и false в обратном случае.
     */
    bool are_trees_equal(const tree_node* tree_node1, const tree_node* tree_node2) const {
        if (tree_node1 == nullptr && tree_node2 == nullptr) return true;
        if (tree_node1 == nullptr || tree_node2 == nullptr) return false;

        if (tree_node1->key_t != tree_node2->key_t || tree_node1->value_t != tree_node2->value_t) {
            return false;
        }

        return are_trees_equal(tree_node1->left_child, tree_node2->left_child) &&
               are_trees_equal(tree_node1->right_child, tree_node2->right_child);
    }

    /**
     * @brief Ищет узел в дереве.
     * @param input_key Ключ для поиска.
     * @return Указатель на найденный узел, если узла нет - nullptr.
     */
    tree_node* search_node(const key_type& input_key) const {
        tree_node *current = tree_root;
        while (current) {
            if (input_key == current->key_t) return current;
            else if (input_key > current->key_t) current = current->right_child;
            else current = current->left_child;
        }
        return nullptr;
    }

    /**
     * @brief Вставляет узел в дерево.
     * @param current Текущий корень.
     * @param input_key Ключ для вставки.
     * @param input_value Значение для вставки.
     * @details Рекурсивно находит позицию для вставки нового узла согласно правилам бинарного дерева поиска,
     *          затем обновляет высоты предков и выполняет балансировку для сохранения свойств AVL-дерева.
     * @return Указатель на корень поддерева.
     * @see insert_helper
     */
    tree_node* insert_node(tree_node* current,const key_type& input_key, const value_type& input_value) {
        if (!current) return new tree_node(input_key, input_value);
        if (input_key < current->key_t) current->left_child = insert_node(current->left_child, input_key, input_value);
        else current->right_child = insert_node(current->right_child,  input_key, input_value);
        update_height(current);
        return balance(current);
    }

    /**
     * @brief Удаляет узел с одним потомком или без потомков.
     * @param current Узел для удаления.
     * @return Указатель на узел, ставший на место текущего.
     */
    tree_node* delete_simple_node(tree_node* current) {
        tree_node *temporary = current->left_child ? current->left_child : current->right_child;
        if (!temporary) {
            temporary = current;
            current = nullptr;
        } else *current = *temporary;
        delete temporary;
        return current;
    }

    /**
     * @brief Удаляет узел.
     * @param current Текущий корень.
     * @param input_key Ключ удаляемого узла.
     * @details Рекурсивно находит узел с заданным ключом, удаляет его согласно правилам BST,
     *          затем обновляет высоты и выполняет балансировку для сохранения свойств AVL-дерева.
     * @return Указатель на текущий корень.
     * @see delete_helper
     * @see delete_simple_node
     */
    tree_node* delete_node(tree_node* current, const key_type& input_key) {
        if (!current) return nullptr;
        if (input_key < current->key_t) current->left_child = delete_node(current->left_child, input_key);
        else if (input_key > current->key_t) current->right_child = delete_node(current->right_child, input_key);
        else {
            if (!current->left_child || !current->right_child) {
                current = delete_simple_node(current);
            } else {
                tree_node *temporary = current->right_child;
                while (temporary->left_child) {
                    temporary = temporary->left_child;
                }
                current->copy_data(temporary);
                current->right_child = delete_node(current->right_child, temporary->key_t);
            }
        }
        update_height(current);
        return balance(current);
    }

    /**
     * @brief Рекурсивно удаляет дерево.
     * @param current Текущий корень.
     * @see clear_tree
     */
    void clear_helper(tree_node* current){
        if(!current) return;
        clear_helper(current->left_child);
        clear_helper(current->right_child);
        delete current;
    }

    /**
     * @brief Обертка для функции удаления.
     * @see clear_helper
     */
    void clear_tree(){
        if (tree_root) {
            clear_helper(tree_root);
            tree_root=nullptr;
        }
    }

    /**
     * @brief Считает все узлы в дереве.
     * @param current Текущий корень.
     * @param counter Счетчик узлов.
     * @return Количество узлов в дереве.
     * @see get_size
     */
    int tree_size(tree_node* current, int& counter) const {
        if (current) {
            counter++;
            if (current->left_child || current->right_child) {
                counter = tree_size(current->left_child, counter);
                counter = tree_size(current->right_child, counter);
            }
        }
        return counter;
    }

    /**
     * @brief Копирует дерево.
     * @param current Корень исходного дерева для копирования.
     * @return Указатель на корень нового дерева.
     */
    tree_node* copy_tree(const tree_node* current) {
        if (!current) return nullptr;
        tree_node *new_node = new tree_node(current->key_t, current->value_t);
        new_node->node_height = current->node_height;
        new_node->left_child = copy_tree(current->left_child);
        new_node->right_child = copy_tree(current->right_child);
        return new_node;
    }

    template<typename function>
    /**
     * @brief Выполняет центрированный обход дерева.
     * @param current Текущий узел для обхода.
     * @param function_ Функция или функтор, применяемый к ключу и значению каждого узла.
     *                  Должен иметь вид: void(const key_type&, const value_type&).
     * @details Обходит дерево в порядке: левое поддерево -> текущий узел -> правое поддерево.
     */
    void inorder_traverse_helper(tree_node* current, function& function_) const {
        if (!current) return;
        inorder_traverse_helper(current->left_child, function_);
        function_(current->key_t, current->value_t);
        inorder_traverse_helper(current->right_child, function_);
    }

public:

    /**
     * @brief Конструктор по умолчанию.
     */
    binary_tree() : tree_root(nullptr) {}

    /**
     * @brief Деструктор. Освобождает занятую память.
     */
    ~binary_tree() {
        clear_tree();
    }

    /**
     * @brief Конструктор копирования.
     * @param other Корень другого дерева для копирования
     */
    binary_tree(const binary_tree& other) : tree_root(nullptr) {
        if (other.tree_root) {
            tree_root = copy_tree(other.tree_root);
        }
    }

    /**
     * @brief Выполняет обход всего дерева в отсортированном порядке.
     * @param function_ Функция, которая будет вызвана для каждого узла.
     *                  Должна принимать параметры: (const key_type&, const value_type&)
     * @details Публичный интерфейс для центрированного обхода.
     *          Применяет переданную функцию к ключу и значению каждого узла
     *          в порядке возрастания ключей.
     * @see inorder_traverse_helper
     */
    template<typename function>
    void inorder_traverse(function function_) const {
        inorder_traverse_helper(tree_root, function_);
    }

    /**
     * @brief Оператор присваивания
     * @param[in] other Словарь для присваивания
     * @return Ссылка на текущий объект дерева
     */
    binary_tree& operator=(const binary_tree& other) {
        if (this != &other) {
            clear_tree();
            this->tree_root = copy_tree(other.tree_root);
        }
        return *this;
    }

    /**
     * @brief Получает корень дерева.
     * @return Указатель на корень дерева.
     */
    tree_node* get_tree_root() const {
        return tree_root;
    }

    /**
     * @brief Оператор сравнения деревьев на равенство
     * @param[in] other Дерево для сравнения
     * @return true если деревья идентичны, false в противном случае
     * @see operator!=
     * @see are_trees_equal
     */
    bool operator==(const binary_tree& other) const {
        return are_trees_equal(tree_root, other.tree_root);
    }

    /**
     * @brief Оператор сравнения деревьев на неравенство.
     * @param[in] other Дерево для сравнения.
     * @return true если деревья не равны, false в противном случае.
     * @see operator==
     */
    bool operator!=(const binary_tree& other) const {
        return !(*this == other);
    }

    /**
     * @brief Вспомогательная функция для вставки узла.
     * @param key_to_insert Ключ для вставки.
     * @param value_to_insert Значение для вставки.
     * @return true, если узла с таким ключом в дереве нет, и false в противном случае.
     * @see insert_node
     */
    bool insert_helper(const key_type& key_to_insert, const value_type& value_to_insert) {
        if(search_node(key_to_insert)) return false;
        tree_root = insert_node(tree_root, key_to_insert, value_to_insert);
        return true;
    }

    /**
     * @brief Вспомогательная функция для удаления узла.
     * @param key_to_insert Ключ для удаления.
     * @return true, если узел с таким ключом в дереве есть, и false в противном случае.
     */
    bool delete_helper(const key_type& key_to_delete) {
        if(!search_node(key_to_delete)) return false;
        tree_root = delete_node(tree_root, key_to_delete);
        return true;
    }

    /**
     * @brief Внешняя функция для определения размер дерева.
     * @return Количество узлов в дереве.
     * @see tree_size
     */
    int get_size() const {
        int word_counter = 0;
        int number = tree_size(tree_root, word_counter);
        return number;
    }

    /**
     * @brief Внешняя функция для определения принадлежности узла дереву.
     * @param key_to_find Ключ для поиска.
     * @return true, если дерево содержит узел с заданным ключом, false в противном случае.
     * @see search_node
     */
    bool contains_node(const key_type& key_to_find) const {
        return search_node(key_to_find);
    }

    /**
     * @brief Получает значение узла по ключу.
     * @param key_to_find Ключ для поиска.
     * @return Значение узла, если он есть в дереве, и бросает ошибку в противном случае.
     * @details Константная версия
     */
    const value_type& get_value(const key_type& key_to_find) const {
        tree_node *temporary = search_node(key_to_find);
        if (temporary) return temporary->value_t;
        else throw std::out_of_range("Ключ не найден.");
    }

    /**
     * @brief Получает значение узла для изменения.
     * @param key_to_find Ключ для поиска.
     * @return Значение узла, если он есть в дереве, и бросает ошибку в противном случае.
     * @details Неконстантная версия
     */
    value_type& get_value(const key_type& key_to_find) {
        tree_node *temporary = search_node(key_to_find);
        if (temporary) return temporary->value_t;
        else throw std::out_of_range("Ключ не найден.");
    }

    /**
     * @brief Печатает содержимое дерева.
     * @param[out] output Выходной поток.
     * @param[in] current Корень дерева для печати.
     * @param counter Счетчик узлов.
     * @return Счетчик.
     */
    int print_dictionary(std::ostream& output, tree_node* current, int& counter) const {
        if (current) {
            counter = print_dictionary(output, current->left_child, counter);
            counter++;
            output << counter << ". ";
            output << *current;
            counter = print_dictionary(output, current->right_child, counter);
        }
        return counter;
    }

    /**
     * @brief Проверка пустоты дерева.
     * @return true если дерево пусто, false в противном случае.
     * @see get_tree_root
     */
    bool empty_tree() const {
        return !get_tree_root();
    }
};

#endif //SEM3_L1_PPOIS_BINARY_TREE_H
