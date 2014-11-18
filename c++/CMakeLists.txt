cmake_minimum_required(VERSION 2.8.4)
project(Monopoly)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -v -stdlib=libc++")

add_subdirectory(src)
