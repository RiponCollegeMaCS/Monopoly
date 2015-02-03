cmake_minimum_required(VERSION 2.8.4)
project(Monopoly)

add_definitions("-I${CMAKE_CURRENT_SOURCE_DIR}/include")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(EXECUTABLE_OUTPUT_PATH bin)

add_subdirectory(src build)
