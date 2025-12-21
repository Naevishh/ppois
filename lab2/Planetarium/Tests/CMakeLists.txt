project(Tests)

add_executable(Tests
        ServiceTest.cpp
        PeopleTest.cpp
        FacadeTest.cpp
        SkyTest.cpp
        ValidationTest.cpp
        EventsTest.cpp
        InventoryTest.cpp
        UtilsTest.cpp
)

target_include_directories(Tests PRIVATE
        ${CMAKE_SOURCE_DIR}/Events
        ${CMAKE_SOURCE_DIR}/Exceptions
        ${CMAKE_SOURCE_DIR}/Facade
        ${CMAKE_SOURCE_DIR}/Inventory
        ${CMAKE_SOURCE_DIR}/People
        ${CMAKE_SOURCE_DIR}/Service
        ${CMAKE_SOURCE_DIR}/Sky
        ${CMAKE_SOURCE_DIR}/Utils
        ${CMAKE_SOURCE_DIR}/Validation
)

target_link_libraries(Tests
        Facade
        Events
        Inventory
        People
        Service
        Sky
        Utils
        Validation
        Exceptions
)