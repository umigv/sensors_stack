cmake_minimum_required(VERSION 2.8.3)

project(sensors_scripts)

find_package(catkin REQUIRED)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

install(PROGRAMS scripts/run_velodyne.sh 
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(PROGRAMS scripts/garmin_setup.sh 
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})


