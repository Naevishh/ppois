project(Tests)

add_executable(Tests
        set_tests.cpp
        set_manager_tests.cpp
        string_validator_tests.cpp
)

target_include_directories(Tests PRIVATE
        ${CMAKE_SOURCE_DIR}/Cantor_set
)

target_link_libraries(Tests
        Cantor_set
)