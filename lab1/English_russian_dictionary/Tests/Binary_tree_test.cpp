#include <gtest/gtest.h>
#include <string>
#include <map>
#include "Binary_tree.h"

using namespace std;

class BinaryTreeTest : public ::testing::Test {
protected:
    void SetUp() override {

        tree1.insert_helper(5, "five");
        tree1.insert_helper(3, "three");
        tree1.insert_helper(7, "seven");

        tree2.insert_helper(10, "ten");
        tree2.insert_helper(5, "five");
        tree2.insert_helper(15, "fifteen");
    }

    void TearDown() override {
        // Очистка после тестов
    }

    binary_tree<int, string> empty_tree;
    binary_tree<int, string> tree1;
    binary_tree<int, string> tree2;
};

TEST_F(BinaryTreeTest, DefaultConstructor) {
    EXPECT_TRUE(empty_tree.empty_tree());
    EXPECT_EQ(empty_tree.get_size(), 0);
    EXPECT_EQ(empty_tree.get_tree_root(), nullptr);
}

TEST_F(BinaryTreeTest, CopyConstructor) {
    binary_tree<int, string> copied_tree(tree1);

    EXPECT_FALSE(copied_tree.empty_tree());
    EXPECT_EQ(copied_tree.get_size(), tree1.get_size());
    EXPECT_TRUE(copied_tree == tree1);
}

TEST_F(BinaryTreeTest, CopyConstructorEmpty) {
    binary_tree<int, string> copied_tree(empty_tree);

    EXPECT_TRUE(copied_tree.empty_tree());
    EXPECT_EQ(copied_tree.get_size(), 0);
}

TEST_F(BinaryTreeTest, AssignmentOperator) {
    binary_tree<int, string> assigned_tree;
    assigned_tree = tree1;

    EXPECT_FALSE(assigned_tree.empty_tree());
    EXPECT_EQ(assigned_tree.get_size(), tree1.get_size());
    EXPECT_TRUE(assigned_tree == tree1);
}

TEST_F(BinaryTreeTest, SelfAssignment) {
    tree1 = tree1;

    EXPECT_FALSE(tree1.empty_tree());
    EXPECT_EQ(tree1.get_size(), 3);
}

TEST_F(BinaryTreeTest, AssignmentOperatorEmpty) {
    binary_tree<int, string> assigned_tree;
    assigned_tree = empty_tree;

    EXPECT_TRUE(assigned_tree.empty_tree());
    EXPECT_EQ(assigned_tree.get_size(), 0);
}

TEST_F(BinaryTreeTest, InsertNewElement) {
    EXPECT_TRUE(empty_tree.insert_helper(1, "one"));
    EXPECT_FALSE(empty_tree.empty_tree());
    EXPECT_EQ(empty_tree.get_size(), 1);
    EXPECT_TRUE(empty_tree.contains_node(1));
}

TEST_F(BinaryTreeTest, InsertDuplicateElement) {
    EXPECT_TRUE(tree1.insert_helper(10, "ten"));
    EXPECT_FALSE(tree1.insert_helper(10, "ten_duplicate")); // Дубликат не должен вставиться
    EXPECT_EQ(tree1.get_size(), 4); // Размер должен остаться 4 (3 исходных + 1 новый)
}

TEST_F(BinaryTreeTest, InsertMultipleElements) {
    binary_tree<int, string> tree;

    EXPECT_TRUE(tree.insert_helper(50, "fifty"));
    EXPECT_TRUE(tree.insert_helper(25, "twenty_five"));
    EXPECT_TRUE(tree.insert_helper(75, "seventy_five"));
    EXPECT_TRUE(tree.insert_helper(10, "ten"));
    EXPECT_TRUE(tree.insert_helper(30, "thirty"));

    EXPECT_EQ(tree.get_size(), 5);
    EXPECT_TRUE(tree.contains_node(50));
    EXPECT_TRUE(tree.contains_node(25));
    EXPECT_TRUE(tree.contains_node(75));
    EXPECT_TRUE(tree.contains_node(10));
    EXPECT_TRUE(tree.contains_node(30));
}

TEST_F(BinaryTreeTest, DeleteExistingElement) {
    EXPECT_TRUE(tree1.delete_helper(3));
    EXPECT_FALSE(tree1.contains_node(3));
    EXPECT_EQ(tree1.get_size(), 2);
}

TEST_F(BinaryTreeTest, DeleteNonExistingElement) {
    EXPECT_FALSE(tree1.delete_helper(999));
    EXPECT_EQ(tree1.get_size(), 3);
}

TEST_F(BinaryTreeTest, DeleteRootElement) {
    EXPECT_TRUE(tree1.delete_helper(5));
    EXPECT_FALSE(tree1.contains_node(5));
    EXPECT_EQ(tree1.get_size(), 2);
}

TEST_F(BinaryTreeTest, DeleteAllElements) {
    EXPECT_TRUE(tree1.delete_helper(3));
    EXPECT_TRUE(tree1.delete_helper(7));
    EXPECT_TRUE(tree1.delete_helper(5));

    EXPECT_TRUE(tree1.empty_tree());
    EXPECT_EQ(tree1.get_size(), 0);
}

TEST_F(BinaryTreeTest, DeleteFromEmptyTree) {
    EXPECT_FALSE(empty_tree.delete_helper(1));
}

TEST_F(BinaryTreeTest, ContainsExistingElement) {
    EXPECT_TRUE(tree1.contains_node(5));
    EXPECT_TRUE(tree1.contains_node(3));
    EXPECT_TRUE(tree1.contains_node(7));
}

TEST_F(BinaryTreeTest, ContainsNonExistingElement) {
    EXPECT_FALSE(tree1.contains_node(999));
    EXPECT_FALSE(empty_tree.contains_node(1));
}

TEST_F(BinaryTreeTest, GetValueExistingElement) {
    EXPECT_EQ(tree1.get_value(5), "five");
    EXPECT_EQ(tree1.get_value(3), "three");
    EXPECT_EQ(tree1.get_value(7), "seven");
}

TEST_F(BinaryTreeTest, GetValueNonExistingElement) {
    EXPECT_THROW(tree1.get_value(999), std::out_of_range);
    EXPECT_THROW(empty_tree.get_value(1), std::out_of_range);
}

TEST_F(BinaryTreeTest, GetValueModifyElement) {
    tree1.get_value(5) = "FIVE_MODIFIED";
    EXPECT_EQ(tree1.get_value(5), "FIVE_MODIFIED");
}

TEST_F(BinaryTreeTest, SizeOperations) {
    EXPECT_EQ(empty_tree.get_size(), 0);
    EXPECT_EQ(tree1.get_size(), 3);

    tree1.insert_helper(10, "ten");
    EXPECT_EQ(tree1.get_size(), 4);

    tree1.delete_helper(10);
    EXPECT_EQ(tree1.get_size(), 3);
}

TEST_F(BinaryTreeTest, EmptyOperations) {
    EXPECT_TRUE(empty_tree.empty_tree());
    EXPECT_FALSE(tree1.empty_tree());

    empty_tree.insert_helper(1, "one");
    EXPECT_FALSE(empty_tree.empty_tree());

    empty_tree.delete_helper(1);
    EXPECT_TRUE(empty_tree.empty_tree());
}

TEST_F(BinaryTreeTest, EqualityOperator) {
    binary_tree<int, string> tree_copy = tree1;
    EXPECT_TRUE(tree1 == tree_copy);

    tree_copy.insert_helper(10, "ten");
    EXPECT_FALSE(tree1 == tree_copy);
}

TEST_F(BinaryTreeTest, InequalityOperator) {
    EXPECT_TRUE(tree1 != tree2);

    binary_tree<int, string> tree_copy = tree1;
    EXPECT_FALSE(tree1 != tree_copy);
}

// Тесты обхода дерева
TEST_F(BinaryTreeTest, InorderTraversal) {
    map<int, string> result;
    auto collect_function = [&result](int key, const string& value) {
        result[key] = value;
    };

    tree1.inorder_traverse(collect_function);

    EXPECT_EQ(result.size(), 3);
    EXPECT_EQ(result[3], "three");
    EXPECT_EQ(result[5], "five");
    EXPECT_EQ(result[7], "seven");

    vector<int> keys;
    for (const auto& pair : result) {
        keys.push_back(pair.first);
    }
    EXPECT_TRUE(is_sorted(keys.begin(), keys.end()));
}

TEST_F(BinaryTreeTest, InorderTraversalEmpty) {
    bool was_called = false;
    auto function = [&was_called](int key, const string& value) {
        was_called = true;
    };

    empty_tree.inorder_traverse(function);
    EXPECT_FALSE(was_called);
}

TEST_F(BinaryTreeTest, TreeBalancing) {
    binary_tree<int, string> tree;

    tree.insert_helper(1, "one");
    tree.insert_helper(2, "two");
    tree.insert_helper(3, "three");
    tree.insert_helper(4, "four");
    tree.insert_helper(5, "five");

    EXPECT_EQ(tree.get_size(), 5);

    for (int i = 1; i <= 5; ++i) {
        EXPECT_TRUE(tree.contains_node(i));
    }

    vector<int> traversal_result;
    auto traversal_function = [&traversal_result](int key, const string& value) {
        traversal_result.push_back(key);
    };

    tree.inorder_traverse(traversal_function);

    EXPECT_EQ(traversal_result.size(), 5);
    EXPECT_TRUE(is_sorted(traversal_result.begin(), traversal_result.end()));
}

TEST_F(BinaryTreeTest, ComplexOperationsSequence) {
    binary_tree<int, string> tree;

    EXPECT_TRUE(tree.insert_helper(50, "50"));
    EXPECT_TRUE(tree.insert_helper(25, "25"));
    EXPECT_TRUE(tree.insert_helper(75, "75"));
    EXPECT_TRUE(tree.insert_helper(10, "10"));
    EXPECT_TRUE(tree.insert_helper(30, "30"));
    EXPECT_TRUE(tree.insert_helper(60, "60"));
    EXPECT_TRUE(tree.insert_helper(80, "80"));

    EXPECT_EQ(tree.get_size(), 7);

    EXPECT_TRUE(tree.delete_helper(25));
    EXPECT_TRUE(tree.delete_helper(75));

    EXPECT_EQ(tree.get_size(), 5);
    EXPECT_FALSE(tree.contains_node(25));
    EXPECT_FALSE(tree.contains_node(75));

    EXPECT_TRUE(tree.insert_helper(35, "35"));
    EXPECT_TRUE(tree.insert_helper(65, "65"));

    EXPECT_EQ(tree.get_size(), 7);

    vector<pair<int, string>> expected = {
            {10, "10"}, {30, "30"}, {35, "35"}, {50, "50"},
            {60, "60"}, {65, "65"}, {80, "80"}
    };

    vector<pair<int, string>> actual;
    auto collect_function = [&actual](int key, const string& value) {
        actual.emplace_back(key, value);
    };

    tree.inorder_traverse(collect_function);

    EXPECT_EQ(actual.size(), expected.size());
    for (size_t i = 0; i < expected.size(); ++i) {
        EXPECT_EQ(actual[i].first, expected[i].first);
        EXPECT_EQ(actual[i].second, expected[i].second);
    }
}

TEST(BinaryTreeDifferentTypesTest, StringKeyIntValue) {
    binary_tree<string, int> tree;

    EXPECT_TRUE(tree.insert_helper("apple", 10));
    EXPECT_TRUE(tree.insert_helper("banana", 20));
    EXPECT_TRUE(tree.insert_helper("cherry", 30));

    EXPECT_EQ(tree.get_size(), 3);
    EXPECT_TRUE(tree.contains_node("banana"));
    EXPECT_EQ(tree.get_value("cherry"), 30);

    EXPECT_TRUE(tree.delete_helper("apple"));
    EXPECT_FALSE(tree.contains_node("apple"));
}

TEST(BinaryTreeDifferentTypesTest, DoubleKey) {
    binary_tree<double, string> tree;

    EXPECT_TRUE(tree.insert_helper(1.5, "one_point_five"));
    EXPECT_TRUE(tree.insert_helper(2.7, "two_point_seven"));
    EXPECT_TRUE(tree.insert_helper(0.3, "zero_point_three"));

    EXPECT_EQ(tree.get_size(), 3);
    EXPECT_TRUE(tree.contains_node(1.5));

    vector<double> keys;
    auto collect_function = [&keys](double key, const string& value) {
        keys.push_back(key);
    };

    tree.inorder_traverse(collect_function);
    EXPECT_TRUE(is_sorted(keys.begin(), keys.end()));
}

TEST_F(BinaryTreeTest, EmptyTreeOperations) {
    EXPECT_THROW(empty_tree.get_value(1), std::out_of_range);
    EXPECT_FALSE(empty_tree.delete_helper(1));
    EXPECT_FALSE(empty_tree.contains_node(1));
}
