#include "set_manager.h"
#include <iostream>
#include <vector>

bool set_manager::create_set(const std::string& elements) {
    if(find_set(elements)!=-1) return false;
    set_list.emplace_back(elements);
    return true;
}

bool set_manager::delete_set(size_t set_index) {
    if (set_index >= set_list.size()) return false;
    set_list.erase(set_list.begin() + set_index);
    return true;
}

size_t set_manager::find_set(const std::string& elements){
    cantor_set cantor_set_(elements);
    for (size_t i = 0; i < set_manager::set_list.size(); ++i){
        if (set_manager::set_list[i]==cantor_set_) return i;
    }
    return -1;
}

bool set_manager::create_set_help(const std::string& elements){
    return create_set(elements);
}

bool set_manager::delete_set_help(size_t set_number){
    return delete_set(set_number-1);
}

cantor_set& set_manager::get_set(size_t index) {
    return set_list[index];
}

size_t set_manager::get_set_count() const {
    return set_list.size();
}

std::vector<std::string> set_manager::list_all_sets() const {
    std::vector<std::string> set_list_to_print;
    set_list_to_print.reserve(set_list.size());
    for (const cantor_set &set : set_list) {
        set_list_to_print.push_back(cantor_set::print_helper(set));
    }
    return set_list_to_print;
}

cantor_set set_manager::union_sets(size_t index_1, size_t index_2) {
    cantor_set result = set_list[index_1] + set_list[index_2];
    return result;
}

cantor_set set_manager::intersection_sets(size_t index_1, size_t index_2) {
    cantor_set result = set_list[index_1] * set_list[index_2];
    return result;
}

cantor_set set_manager::difference_sets(size_t index_1, size_t index_2) {
    cantor_set result = set_list[index_1] - set_list[index_2];
    return result;
}

cantor_set set_manager::set_boolean(size_t set_index) {
    cantor_set result = set_list[set_index].set_boolean(set_list[set_index]);
    return result;
}