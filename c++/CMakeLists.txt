cmake_minimum_required(VERSION 2.8.4)
project(Monopoly)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(EXECUTABLE_OUTPUT_PATH bin)

add_subdirectory(src build)
