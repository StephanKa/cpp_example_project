include(FetchContent)

find_package(Slint QUIET)
if(NOT Slint_FOUND)
    message(STATUS "Slint could not be located in the CMake module search path. Downloading it from Git and building it locally")
    FetchContent_Declare(
            Slint
            GIT_REPOSITORY https://github.com/slint-ui/slint.git
            GIT_TAG v1.9.2  # pin to a specific release for reproducible builds
            SOURCE_SUBDIR api/cpp
            GIT_SHALLOW TRUE  # faster clone, no full history needed
    )
    FetchContent_MakeAvailable(Slint)
endif()

add_executable(slintExample src/main.cpp)
target_link_libraries(slintExample PRIVATE project_options project_warnings Slint::Slint)
slint_target_sources(slintExample ui/app-window.slint)
# On Windows, copy the Slint DLL next to the application binary so that it's found.
if(WIN32)
    add_custom_command(TARGET slintExample POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:slintExample> $<TARGET_FILE_DIR:slintExample> COMMAND_EXPAND_LISTS)
endif()
