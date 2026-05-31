find_package(sml REQUIRED)
find_package(spdlog REQUIRED)

add_executable(test_sml main.cpp logger.h states.h events.h plantumlDump.h actions.h)
target_link_libraries(test_sml PRIVATE project_options project_warnings sml::sml spdlog::spdlog_header_only)
