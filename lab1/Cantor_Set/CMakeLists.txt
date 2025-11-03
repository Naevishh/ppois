cmake_minimum_required(VERSION 3.27)
project(sem3_l1_ppois_p2)

set(CMAKE_CXX_STANDARD 17)

add_executable(sem3_l1_ppois_p2 main.cpp
        Cantor_set/string_validator.h
        Cantor_set/string_validator.cpp
        Cantor_set/set_manager.h
        Cantor_set/set_manager.cpp
        Cantor_set/set.h
        Cantor_set/set.cpp

)

add_subdirectory(Tests)
add_subdirectory(Cantor_set)

target_link_libraries(sem3_l1_ppois_p2
        Cantor_set
)

add_subdirectory(googletest-main)
enable_testing()
include(GoogleTest)
target_link_libraries(Tests GTest::gtest_main)