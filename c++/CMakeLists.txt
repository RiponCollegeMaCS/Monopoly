cmake_minimum_required(VERSION 3.0)

add_subdirectory(src build)

#set(EXECUTABLE_OUTPUT_PATH bin)

target_include_directories(monopoly PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

target_compile_options(monopoly PUBLIC "-std=c++11")
#target_compile_options(monopoly PUBLIC "$<$<PLATFORM_ID:LINUX>:-lpthread>")

option(OPTIMIZATIONS "Compile with -O3" ON)

target_compile_options(monopoly PUBLIC "$<$<BOOL:OPTIMIZATIONS>:-O3>")
## command line build/compile options
# build as library, e.g. for Julia
option(LIBRARY_BUILD "Build and link as library" OFF)

target_compile_options(monopoly PUBLIC "$<$<BOOL:LIBRARY_BUILD>:-shared>")
target_compile_options(monopoly PUBLIC "$<$<BOOL:LIBRARY_BUILD>:-fPIC>")

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
