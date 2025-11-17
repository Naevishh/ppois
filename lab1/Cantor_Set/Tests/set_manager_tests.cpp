#include <gtest/gtest.h>
#include "set_manager.h"
#include "set.h"


class SetManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        manager.create_set_help("{a,b,c}");
        manager.create_set_help("{e,f,g}");
    }

    void TearDown() override {
    }

    set_manager manager;
};

TEST_F(SetManagerTest, CreateSetValid) {
    EXPECT_TRUE(manager.create_set_help("{h,i,j}"));
    EXPECT_EQ(manager.get_set_count(), 3);
}

TEST_F(SetManagerTest, CreateSetDuplicate) {
    EXPECT_FALSE(manager.create_set_help("{a,b,c}"));
}

TEST_F(SetManagerTest, DeleteSetValid) {
    EXPECT_TRUE(manager.delete_set_help(1));
    EXPECT_EQ(manager.get_set_count(), 1);
}

TEST_F(SetManagerTest, DeleteSetInvalid) {
    EXPECT_FALSE(manager.delete_set_help(5));
}

TEST_F(SetManagerTest, GetSetCount) {
    EXPECT_EQ(manager.get_set_count(), 2);
}

TEST_F(SetManagerTest, GetSetValid) {
    cantor_set& set = manager.get_set(0);
    EXPECT_FALSE(set.is_empty());
}

TEST_F(SetManagerTest, ListAllSets) {
    std::vector<std::string> sets = manager.list_all_sets();
    EXPECT_EQ(sets.size(), 2);
}

TEST_F(SetManagerTest, UnionSets) {
    cantor_set result = manager.union_sets(0, 1);
    EXPECT_FALSE(result.is_empty());
}

TEST_F(SetManagerTest, IntersectionSets) {
    cantor_set result = manager.intersection_sets(0, 1);
    EXPECT_TRUE(result.is_empty());
}

TEST_F(SetManagerTest, DifferenceSets) {
    cantor_set result = manager.difference_sets(0, 1);
    EXPECT_FALSE(result.is_empty());
}

TEST_F(SetManagerTest, SetBoolean) {
    cantor_set result = manager.set_boolean(0);
    EXPECT_FALSE(result.is_empty());
}

TEST_F(SetManagerTest, FindSetExists) {
    set_manager local_manager;
    local_manager.create_set_help("{k,l,m}");
    EXPECT_NE(local_manager.get_set_count(), 0);
}

TEST_F(SetManagerTest, FindSetNotExists) {
    set_manager local_manager;
    local_manager.create_set_help("{n,o}");
    EXPECT_EQ(local_manager.get_set_count(), 1);
}

TEST_F(SetManagerTest, MultipleOperations) {
    set_manager local_manager;
    EXPECT_TRUE(local_manager.create_set_help("{a,b}"));
    EXPECT_TRUE(local_manager.create_set_help("{c,d}"));
    EXPECT_EQ(local_manager.get_set_count(), 2);

    cantor_set union_result = local_manager.union_sets(0, 1);
    EXPECT_FALSE(union_result.is_empty());

    EXPECT_TRUE(local_manager.delete_set_help(1));
    EXPECT_EQ(local_manager.get_set_count(), 1);
}

TEST_F(SetManagerTest, BoundaryConditions) {
    set_manager local_manager;
    EXPECT_FALSE(local_manager.delete_set_help(0));
    EXPECT_FALSE(local_manager.delete_set_help(1));

    EXPECT_TRUE(local_manager.create_set_help("{}"));
    EXPECT_EQ(local_manager.get_set_count(), 1);
}
