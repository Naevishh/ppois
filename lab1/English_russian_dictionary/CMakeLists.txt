cmake_minimum_required(VERSION 3.27)
project(sem3_l1_ppois)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fprofile-arcs -ftest-coverage")

set(CMAKE_CXX_STANDARD 17)

add_executable(sem3_l1_ppois main.cpp
        Dictionary/Dictionary.h
        Dictionary/Dictionary.cpp
        Dictionary/String_validator.h
        Dictionary/String_validator.cpp

)

add_subdirectory(Tests)
add_subdirectory(Dictionary)

target_link_libraries(sem3_l1_ppois
    Dictionary
)

add_subdirectory(googletest-main)
enable_testing()
include(GoogleTest)
target_link_libraries(Tests GTest::gtest_main)