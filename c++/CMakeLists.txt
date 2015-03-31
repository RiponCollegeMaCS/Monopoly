cmake_minimum_required(VERSION 2.8.9)
project(Monopoly)

add_definitions("-I${CMAKE_CURRENT_SOURCE_DIR}/include")
if(APPLE)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
else()
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -std=c++11")
endif()
set(EXECUTABLE_OUTPUT_PATH bin)

add_subdirectory(src build)

## command line build/compile options
# build as library, e.g. for Julia
option(LIBRARY_BUILD "Build and link as library" OFF)

if(LIBRARY_BUILD)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -shared -fPIC")
endif()

option(OPTIMIZATIONS "Compile with -O3" ON)

if(OPTIMIZATIONS)
	set(CMAKE_CXX_FLAGS "-O3 ${CMAKE_CXX_FLAGS}")
endif()

## add a target to generate API documentation with Doxygen
find_package(Doxygen)
if(DOXYGEN_FOUND)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY)
add_custom_target(doc
${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
COMMENT "Generating API documentation with Doxygen" VERBATIM
)
endif(DOXYGEN_FOUND)
