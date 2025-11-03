#include <iostream>
#include <string>
#include <variant>
#include "set.h"

cantor_set cantor_set::initialize_set_elems(const std::string &elements_string,const char &start_brace ,size_t &position) {
    cantor_set set_to_initialize(elements_string[0]);
    char end_brace = (start_brace == '{') ? '}' : '>';
    set_to_initialize.is_directed = start_brace != '{';
    while (position < elements_string.size() && elements_string[position] != end_brace) {
        if (elements_string[position] == '{' || elements_string[position] == '<') {
            position++;
            cantor_set nested_set(elements_string[position-1]);
            nested_set = initialize_set_elems(elements_string, elements_string[position-1], position);
            if(find_element(set_to_initialize, nested_set)==-1)
                set_to_initialize.set_elements.emplace_back(nested_set);
        } else {
            if(find_element(set_to_initialize, elements_string[position])==-1)
                set_to_initialize.set_elements.emplace_back(elements_string[position]);
        }
        position++;
    }
    return set_to_initialize;
}

bool cantor_set::compare_elems(const element &first_elem, const element &second_elem) const {
    if (first_elem.index() == 0 && second_elem.index() == 0)
        return std::get<0>(first_elem) == std::get<0>(second_elem);
    else if (first_elem.index() != second_elem.index()) return false;
    else {
        cantor_set first_set=std::get<1>(first_elem);
        cantor_set second_set=std::get<1>(second_elem);
        if (first_set.set_elements.size() != second_set.set_elements.size() ||
            first_set.is_directed != second_set.is_directed) return false;
        return compare_sets(first_set, second_set);
    }
}

bool cantor_set::compare_sets(const cantor_set &first_set, const cantor_set &second_set) const {
    if (first_set.is_directed){
        for (size_t i = 0; i < first_set.set_elements.size(); ++i) {
            if(!compare_elems(first_set.set_elements[i],
                              second_set.set_elements[i])) return false;
        }
    }else{
        for (const element &first_current: first_set.set_elements){
            bool element_is_equal = false;
            for (const element &second_current : second_set.set_elements){
                element_is_equal=compare_elems(first_current, second_current);
                if(element_is_equal) break;
            }
            if (!element_is_equal) return false;
        }
    }
    return true;
}

int cantor_set::find_element(const cantor_set &cantor_set_, const std::string &input_string){
    element elem_to_find=element_initializer(input_string);
    return find_element(cantor_set_, elem_to_find);
}

int cantor_set::find_element(const std::string &input_string){
    return find_element(*this, input_string);
}

int cantor_set::find_element(const element &elem_to_find){
    return find_element(*this, elem_to_find);
}

int cantor_set::find_element(const cantor_set &cantor_set_, const element &elem_to_find) {
    for (size_t i = 0; i < cantor_set_.set_elements.size(); ++i){
        if(compare_elems(cantor_set_.set_elements[i], elem_to_find)) return i;
    }
    return -1;
}

bool cantor_set::add_element(const element &elem_to_add){
    if(find_element(elem_to_add)!=-1) return false;
    set_elements.push_back(elem_to_add);
    return true;
}

bool cantor_set::add_helper(const std::string& string_to_add){
    element elem_to_add = element_initializer(string_to_add);
    return add_element(elem_to_add);
}

bool cantor_set::delete_element(const element &elem_to_delete){
    int position=find_element(elem_to_delete);
    if(position==-1) return false;
    set_elements.erase(set_elements.begin() + position);
    return true;
}

bool cantor_set::delete_helper(const std::string& string_to_delete){
    element elem_to_delete = element_initializer(string_to_delete);
    return delete_element(elem_to_delete);
}

cantor_set::cantor_set(const char start_brace) {
    start_brace == '{' ? is_directed = false : is_directed = true;
}

cantor_set::cantor_set(const std::string& elements_string) {
    elements_string[0] == '{' ? is_directed = false : is_directed = true;
    *this = std::get<1>(element_initializer(elements_string));
}

cantor_set::cantor_set(const char* elements_string) {
    elements_string[0] == '{' ? is_directed = false : is_directed = true;
    *this = std::get<1>(element_initializer(elements_string));
}

cantor_set::cantor_set(const cantor_set &other_set) {
    is_directed = other_set.is_directed;
    set_elements = other_set.set_elements;
}

cantor_set& cantor_set::operator=(const cantor_set &other_set) {
    if (this != &other_set) {
        this->is_directed = other_set.is_directed;
        this->set_elements = other_set.set_elements;
    }
    return *this;
}

cantor_set::element cantor_set::element_initializer(const std::string &input_string){
    element element_to_initialize;
    if (input_string.size() == 1) element_to_initialize=input_string[0];
    else{
        size_t position = 1;
        element_to_initialize =
                initialize_set_elems(input_string,input_string[0], position);
    }
    return element_to_initialize;
}

bool cantor_set::is_empty(){
    return set_elements.empty();
}

bool cantor_set::is_directed_set() const{
    return is_directed;
}

size_t cantor_set::set_length() {
    return set_elements.size();
}

bool cantor_set::operator==(const cantor_set &other_set) const {
    return compare_elems(other_set, *this);
}

bool cantor_set::operator!=(const cantor_set &other_set) const{
    return !(*this == other_set);
}

std::string cantor_set::print_set(const element &elem_to_print, std::string& printed_set) const {
    if (elem_to_print.index() == 0) {
        printed_set+=std::get<0>(elem_to_print);
    } else {
        cantor_set set_to_print=std::get<1>(elem_to_print);
        (set_to_print.is_directed_set()) ? printed_set+='<' : printed_set+='{';
        for (const element &current_element: std::get<1>(elem_to_print).set_elements) {
            printed_set=print_set(current_element,printed_set);
        }
        if(printed_set[printed_set.size() - 1]==',') printed_set.pop_back();
        (set_to_print.is_directed_set()) ? printed_set+='>' : printed_set+='}';
    }
    printed_set+=',';
    return printed_set;
}

std::string cantor_set::print_helper(const cantor_set &set_to_print){
    std::string printed_set;
    printed_set=set_to_print.print_set(set_to_print, printed_set);
    if(printed_set[printed_set.size() - 1]==',') printed_set.pop_back();
    return printed_set;
}

bool cantor_set::operator[](const std::string &input_string) {
    //element elem_to_find=element_initializer(input_string);
    return find_element(input_string) != -1;
}

cantor_set& cantor_set::operator+=(cantor_set& other_set) {
    for (const auto &current_element: other_set.set_elements) {
        if (find_element(current_element) == -1) set_elements.push_back(current_element);
    }
    return *this;
}

cantor_set cantor_set::operator+(cantor_set& other_set) {
    cantor_set new_set = *this;
    new_set += other_set;
    return new_set;
}

cantor_set& cantor_set::operator*=(cantor_set& other_set) {
    cantor_set result_set('{');
    for (const auto &current_element: set_elements) {
        if (find_element(other_set, current_element) != -1)
            result_set.set_elements.push_back(current_element);
    }
    *this=result_set;
    return *this;
}

cantor_set cantor_set::operator*(cantor_set& other_set) {
    cantor_set new_set = *this;
    new_set *= other_set;
    return new_set;
}

cantor_set& cantor_set::operator-=(cantor_set& other_set) {
    cantor_set result_set('{');
    for (const auto &current_element: set_elements) {
        if (find_element(other_set, current_element) == -1)
            result_set.set_elements.push_back(current_element);
    }
    *this=result_set;
    return *this;
}

cantor_set cantor_set::operator-(cantor_set& other_set) {
    cantor_set new_set = *this;
    new_set -= other_set;
    return new_set;
}

cantor_set cantor_set::set_boolean(cantor_set& other_set) {
    cantor_set result('{');
    cantor_set empty('{');
    result.set_elements.emplace_back(empty);
    for (const auto& element : other_set.set_elements) {
        size_t current_size = result.set_elements.size();
        for (size_t i = 0; i < current_size; ++i) {
            cantor_set new_subset = std::get<1>(result.set_elements[i]);
            new_subset.set_elements.push_back(element);
            result.set_elements.emplace_back(new_subset);
        }
    }
    return result;
}

std::ostream& operator<<(std::ostream& output, const cantor_set &set_to_print) {
    std::string printed_set=cantor_set::print_helper(set_to_print);
    output << printed_set;
    return output;
}

std::istream& operator>>(std::istream& input, cantor_set &set_to_input) {
    std::string input_string;
    std::getline(input, input_string);
    set_to_input=std::get<1>(set_to_input.element_initializer(input_string));
    return input;
}