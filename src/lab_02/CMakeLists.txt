find_package(OpenMP REQUIRED)
add_executable(lab_02 main.cpp)
target_link_libraries(lab_02 PRIVATE matrix OpenMP::OpenMP_CXX)
