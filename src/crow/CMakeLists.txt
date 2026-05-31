find_package(Crow REQUIRED)
find_package(spdlog REQUIRED)

add_executable(test_crow main.cpp)
target_link_libraries(test_crow PRIVATE project_options project_warnings Crow::Crow spdlog::spdlog_header_only)
