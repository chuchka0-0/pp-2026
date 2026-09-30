cmake_minimum_required(VERSION 3.13)
project(pp-2026 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# matrix.hpp доступен всем лабораторным
add_library(matrix INTERFACE)
target_include_directories(matrix INTERFACE ${CMAKE_SOURCE_DIR}/src)

add_subdirectory(src/lab_01)
add_subdirectory(src/lab_02)
add_subdirectory(src/lab_03)
add_subdirectory(src/lab_04)
