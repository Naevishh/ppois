#include <gtest/gtest.h>
#include "set.h"

class CantorSetTest : public ::testing::Test {
protected:
    void SetUp() override {
    }

    void TearDown() override {
    }

    cantor_set createEmptySet() { return cantor_set("{}"); }
    cantor_set createSimpleSet() { return cantor_set("{a,b,c}"); }
    cantor_set createDirectedSet() { return cantor_set("<a,b,c>"); }
};

TEST_F(CantorSetTest, ConstructorFromChar) {
    cantor_set set1('{');
    EXPECT_FALSE(set1.is_directed_set());

    cantor_set set2('<');
    EXPECT_TRUE(set2.is_directed_set());
}

TEST_F(CantorSetTest, ConstructorFromString) {
    cantor_set set1 = createSimpleSet();
    EXPECT_FALSE(set1.is_directed_set());

    cantor_set set2 = createDirectedSet();
    EXPECT_TRUE(set2.is_directed_set());
}

TEST_F(CantorSetTest, ConstructorFromCharArray) {
    cantor_set set1("{a,b,c}");
    EXPECT_FALSE(set1.is_directed_set());

    cantor_set set2("<a,b,c>");
    EXPECT_TRUE(set2.is_directed_set());
}

TEST_F(CantorSetTest, CopyConstructor) {
    cantor_set original = createSimpleSet();
    cantor_set copy(original);
    EXPECT_TRUE(original == copy);
}

TEST_F(CantorSetTest, AssignmentOperator) {
    cantor_set original = createSimpleSet();
    cantor_set copy = original;
    EXPECT_TRUE(original == copy);
}

TEST_F(CantorSetTest, SelfAssignment) {
    cantor_set set = createSimpleSet();
    set = set;
    EXPECT_FALSE(set.is_empty());
}

TEST_F(CantorSetTest, IsEmpty) {
    cantor_set empty_set = createEmptySet();
    EXPECT_TRUE(empty_set.is_empty());

    cantor_set non_empty_set("{a}");
    EXPECT_FALSE(non_empty_set.is_empty());
}

TEST_F(CantorSetTest, SetLength) {
    cantor_set empty_set = createEmptySet();
    EXPECT_EQ(empty_set.set_length(), 0);

    cantor_set set("{abc}");
    EXPECT_EQ(set.set_length(), 3);
}

TEST_F(CantorSetTest, EqualityOperator) {
    cantor_set set1 = createSimpleSet();
    cantor_set set2 = createSimpleSet();
    cantor_set set3("{a,b}");

    EXPECT_TRUE(set1 == set2);
    EXPECT_FALSE(set1 == set3);
}

TEST_F(CantorSetTest, InequalityOperator) {
    cantor_set set1 = createSimpleSet();
    cantor_set set2 = createSimpleSet();
    cantor_set set3("{a,b}");

    EXPECT_FALSE(set1 != set2);
    EXPECT_TRUE(set1 != set3);
}

TEST_F(CantorSetTest, FindElement) {
    cantor_set set = createSimpleSet();

    EXPECT_TRUE(set["a"]);
    EXPECT_TRUE(set["b"]);
    EXPECT_TRUE(set["c"]);
    EXPECT_FALSE(set["d"]);
}

TEST_F(CantorSetTest, AddElement) {
    cantor_set set = createEmptySet();

    EXPECT_TRUE(set.add_helper("a"));
    EXPECT_TRUE(set["a"]);
    EXPECT_FALSE(set.add_helper("a"));
}

TEST_F(CantorSetTest, DeleteElement) {
    cantor_set set = createSimpleSet();

    EXPECT_TRUE(set.delete_helper("a"));
    EXPECT_FALSE(set["a"]);
    EXPECT_FALSE(set.delete_helper("a"));
}

TEST_F(CantorSetTest, UnionOperator) {
    cantor_set set1("{ab}");
    cantor_set set2("{bc}");
    cantor_set result = set1 + set2;

    EXPECT_TRUE(result["a"]);
    EXPECT_TRUE(result["b"]);
    EXPECT_TRUE(result["c"]);
    EXPECT_EQ(result.set_length(), 3);
}

TEST_F(CantorSetTest, UnionAssignmentOperator) {
    cantor_set set1("{ab}");
    cantor_set set2("{bc}");
    set1 += set2;

    EXPECT_TRUE(set1["a"]);
    EXPECT_TRUE(set1["b"]);
    EXPECT_TRUE(set1["c"]);
    EXPECT_EQ(set1.set_length(), 3);
}

TEST_F(CantorSetTest, IntersectionOperator) {
    cantor_set set1("{abc}");
    cantor_set set2("{bcd}");
    cantor_set result = set1 * set2;

    EXPECT_FALSE(result["a"]);
    EXPECT_TRUE(result["b"]);
    EXPECT_TRUE(result["c"]);
    EXPECT_FALSE(result["d"]);
    EXPECT_EQ(result.set_length(), 2);
}

TEST_F(CantorSetTest, IntersectionAssignmentOperator) {
    cantor_set set1("{abc}");
    cantor_set set2("{bcd}");
    set1 *= set2;

    EXPECT_FALSE(set1["a"]);
    EXPECT_TRUE(set1["b"]);
    EXPECT_TRUE(set1["c"]);
    EXPECT_FALSE(set1["d"]);
    EXPECT_EQ(set1.set_length(), 2);
}

TEST_F(CantorSetTest, DifferenceOperator) {
    cantor_set set1("{abcd}");
    cantor_set set2("{bc}");
    cantor_set result = set1 - set2;

    EXPECT_TRUE(result["a"]);
    EXPECT_FALSE(result["b"]);
    EXPECT_FALSE(result["c"]);
    EXPECT_TRUE(result["d"]);
    EXPECT_EQ(result.set_length(), 2);
}

TEST_F(CantorSetTest, DifferenceAssignmentOperator) {
    cantor_set set1("{abcd}");
    cantor_set set2("{bc}");
    set1 -= set2;

    EXPECT_TRUE(set1["a"]);
    EXPECT_FALSE(set1["b"]);
    EXPECT_FALSE(set1["c"]);
    EXPECT_TRUE(set1["d"]);
    EXPECT_EQ(set1.set_length(), 2);
}

TEST_F(CantorSetTest, NestedSets) {
    cantor_set set("{{ab}c}");
    EXPECT_EQ(set.set_length(), 2);

    cantor_set nested_set("{ab}");
    EXPECT_TRUE(set["{a,b}"]);
}

TEST_F(CantorSetTest, DirectedSets) {
    cantor_set set1 = createDirectedSet();
    cantor_set set2 = createDirectedSet();
    cantor_set set3("<a,c,b>");

    EXPECT_TRUE(set1 == set2);
    EXPECT_FALSE(set1 == set3);
}

TEST_F(CantorSetTest, PrintHelper) {
    cantor_set set = createSimpleSet();
    std::string result = cantor_set::print_helper(set);
    EXPECT_FALSE(result.empty());
}

TEST_F(CantorSetTest, OutputStreamOperator) {
    cantor_set set = createSimpleSet();
    std::ostringstream oss;
    oss << set;
    EXPECT_FALSE(oss.str().empty());
}

TEST_F(CantorSetTest, InputStreamOperator) {
    cantor_set set = createEmptySet();
    std::istringstream iss("{x,y,z}");
    iss >> set;

    EXPECT_TRUE(set["x"]);
    EXPECT_TRUE(set["y"]);
    EXPECT_TRUE(set["z"]);
}

TEST_F(CantorSetTest, SetBoolean) {
    cantor_set set("{a,b}");
    cantor_set boolean_set = set.set_boolean(set);

    EXPECT_GT(boolean_set.set_length(), 0);
}

TEST_F(CantorSetTest, ComplexNestedStructures) {
    cantor_set set("{a{bc}{d{ef}}}");
    EXPECT_EQ(set.set_length(), 3);

    EXPECT_TRUE(set["a"]);
    EXPECT_TRUE(set["{b,c}"]);
    EXPECT_TRUE(set["{d,{e,f}}"]);
}

TEST_F(CantorSetTest, DuplicateElements) {
    cantor_set set("{aaab}");
    EXPECT_EQ(set.set_length(), 2);
}

TEST_F(CantorSetTest, EmptyStringElement) {
    cantor_set set1 = createEmptySet();
    cantor_set set2 = createEmptySet();
    EXPECT_TRUE(set1 == set2);
}

TEST_F(CantorSetTest, MixedTypes) {
    cantor_set set("{a{b}c}");
    EXPECT_EQ(set.set_length(), 3);
}
