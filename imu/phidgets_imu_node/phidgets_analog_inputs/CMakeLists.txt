cmake_minimum_required(VERSION 3.5.1)
cmake_policy(SET CMP0048 NEW)
project(phidgets_analog_inputs)

# Use C++14
if (CMAKE_VERSION VERSION_LESS "3.1")
    if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        set(CMAKE_CXX_FLAGS "-std=gnu++14 ${CMAKE_CXX_FLAGS}")
    endif()
else()
    set (CMAKE_CXX_STANDARD 14)
endif()

# High level of warnings:
if (CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra)
endif()

find_package(catkin REQUIRED COMPONENTS nodelet phidgets_api roscpp roslaunch std_msgs)

catkin_package(
    INCLUDE_DIRS include
    LIBRARIES phidgets_analog_inputs
    CATKIN_DEPENDS nodelet phidgets_api roscpp std_msgs
)

include_directories(include ${catkin_INCLUDE_DIRS})

add_library(phidgets_analog_inputs src/analog_inputs_ros_i.cpp)
add_library(phidgets_analog_inputs_nodelet src/phidgets_analog_inputs_nodelet.cpp)

add_dependencies(phidgets_analog_inputs ${catkin_EXPORTED_TARGETS})
add_dependencies(phidgets_analog_inputs_nodelet ${catkin_EXPORTED_TARGETS})

target_link_libraries(phidgets_analog_inputs ${catkin_LIBRARIES})
target_link_libraries(phidgets_analog_inputs_nodelet ${catkin_LIBRARIES} phidgets_analog_inputs)

install(TARGETS phidgets_analog_inputs phidgets_analog_inputs_nodelet
    ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY include/${PROJECT_NAME}/
    DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
    FILES_MATCHING PATTERN "*.h"
)

install(DIRECTORY launch
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(FILES phidgets_analog_inputs_nodelet.xml
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

roslaunch_add_file_check(launch)
