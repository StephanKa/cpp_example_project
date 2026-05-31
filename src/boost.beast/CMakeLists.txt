find_package(Threads)
find_package(fmt REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(Boost REQUIRED)

add_executable(test_boost_beast main.cpp)
target_link_libraries(test_boost_beast PRIVATE project_options project_warnings ${CMAKE_THREAD_LIBS_INIT} Boost::boost nlohmann_json::nlohmann_json fmt::fmt-header-only)
