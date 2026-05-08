INCLUDE(FetchContent)

FIND_PACKAGE(Slint QUIET)
IF(NOT Slint_FOUND)
    MESSAGE(STATUS "Slint could not be located in the CMake module search path. Downloading it from Git and building it locally")
    FETCHCONTENT_DECLARE(
            Slint
            GIT_REPOSITORY https://github.com/slint-ui/slint.git
            GIT_TAG v1.9.2  # pin to a specific release for reproducible builds
            SOURCE_SUBDIR api/cpp
            GIT_SHALLOW TRUE  # faster clone, no full history needed
    )
    FETCHCONTENT_MAKEAVAILABLE(Slint)
ENDIF()

ADD_EXECUTABLE(slintExample src/main.cpp)
TARGET_LINK_LIBRARIES(slintExample PRIVATE Slint::Slint)
SLINT_TARGET_SOURCES(slintExample ui/app-window.slint)
# On Windows, copy the Slint DLL next to the application binary so that it's found.
IF(WIN32)
    ADD_CUSTOM_COMMAND(TARGET slintExample POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:slintExample> $<TARGET_FILE_DIR:slintExample> COMMAND_EXPAND_LISTS)
ENDIF()
