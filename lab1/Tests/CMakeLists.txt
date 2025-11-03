project(Tests)

add_executable(Tests
    DictionaryTest.cpp
        Binary_tree_test.cpp
        String_validator_test.cpp
)

target_include_directories(Tests PRIVATE
    ${CMAKE_SOURCE_DIR}/Dictionary
)

target_link_libraries(Tests
    Dictionary
)