cmake_minimum_required(VERSION 3.25)

# Must be set before project() for the Conan cmake provider
include(cmake/Conan.cmake)

# Disable GNU extensions — avoids conflicts between -Wpedantic and
# -std=c++20 vs -std=gnu++20 when building with PCH enabled
set(CMAKE_CXX_EXTENSIONS OFF)

project(myproject
        LANGUAGES CXX
        VERSION 0.0.1)

include(cmake/ProjectSettings.cmake)
include(cmake/Options.cmake)

# Find Python interpreter for code formatting scripts
find_package(Python3 COMPONENTS Interpreter REQUIRED)
set(Python_EXECUTABLE ${Python3_EXECUTABLE})

include(cmake/BuildingConfig.cmake)
setup_multi_config()

include(cmake/StandardProjectSettings.cmake)
include(cmake/PreventInSourceBuilds.cmake)
include(cmake/CodeFormat.cmake)
include(cmake/InterproceduralOptimization.cmake)
enable_ipo()

# Fetch git hash information for configure version template file
include(cmake/GitInformation.cmake)
get_git_hash()

configure_file("templates/version.hpp.in" "${CMAKE_BINARY_DIR}/generated/include/version.hpp" ESCAPE_QUOTES)

# Link this 'library' to set the c++ standard / compile-time options requested
add_library(project_options INTERFACE)
target_compile_features(project_options INTERFACE cxx_std_${CMAKE_CXX_STANDARD})

# Apply -ftime-trace for build profiling (Clang only)
if(ENABLE_BUILD_WITH_TIME_TRACE)
    target_compile_options(project_options INTERFACE -ftime-trace)
endif()

# Link this 'library' to use the warnings specified in CompilerWarnings.cmake
add_library(project_warnings INTERFACE)

# enable cache system
include(cmake/Cache.cmake)

# standard compiler warnings
include(cmake/CompilerWarnings.cmake)
set_project_warnings(project_warnings)

# sanitizer options if supported by compiler
include(cmake/Sanitizers.cmake)
enable_sanitizers(project_options)

# enable doxygen
include(cmake/Doxygen.cmake)
enable_doxygen()

# allow for static analysis options
include(cmake/StaticAnalyzers.cmake)

# enable precompiled headers
include(cmake/PrecompiledHeader.cmake)
enable_pch()

add_subdirectory(src)

if(CMAKE_CROSSCOMPILING)
    message(STATUS "Tests are not built for cross-compilation targets")
    return()
endif()

if(ENABLE_TESTING)
    enable_testing()
    message(STATUS "Building Tests. Be sure to check out test/constexpr_tests for constexpr testing")
    add_subdirectory(test)
endif()

if(ENABLE_FUZZING)
    message(STATUS "Building Fuzz Tests, using fuzzing sanitizer https://www.llvm.org/docs/LibFuzzer.html")
    add_subdirectory(fuzz_test)
endif()
