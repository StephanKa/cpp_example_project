include(CMakeDependentOption)
cmake_dependent_option(ENABLE_BUILD_WITH_TIME_TRACE
    "Enable -ftime-trace to generate time tracing .json files on clang"
    OFF "NOT MSVC" OFF)

# Very basic PCH example
option(ENABLE_PCH "Enable Precompiled Headers" OFF)

# static analyzers
option(ENABLE_CPPCHECK "Enable static analysis with cppcheck" OFF)
option(ENABLE_CLANG_TIDY "Enable static analysis with clang-tidy" OFF)
option(ENABLE_INCLUDE_WHAT_YOU_USE "Enable static analysis with include-what-you-use" OFF)

# tooling
option(ENABLE_CACHE "Enable cache if available" ON)
option(ENABLE_DOXYGEN "Enable doxygen doc builds of source" OFF)

# Sanitizers
option(ENABLE_SANITIZER_UNDEFINED_BEHAVIOR "Enable undefined behavior sanitizer" OFF)
option(ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" OFF)
option(ENABLE_SANITIZER_LEAK "Enable leak sanitizer" OFF)

# others
option(ENABLE_COVERAGE "Enable coverage reporting for gcc/clang" OFF)
option(ENABLE_IPO "Enable Interprocedural Optimization, aka Link Time Optimization (LTO)" OFF)
option(WARNINGS_AS_ERRORS "Treat compiler warnings as errors" ON)
option(BUILD_SHARED_LIBS "Enable compilation of shared libraries" OFF)
option(ENABLE_TESTING "Enable Test Builds" ON)
option(ENABLE_FUZZING "Enable Fuzzing Builds" OFF)

# Sanitizer mutual-exclusion guards
cmake_dependent_option(ENABLE_SANITIZER_THREAD
    "Enable thread sanitizer"
    OFF "NOT ENABLE_SANITIZER_ADDRESS;NOT ENABLE_SANITIZER_LEAK" OFF)
cmake_dependent_option(ENABLE_SANITIZER_MEMORY
    "Enable memory sanitizer (Clang only)"
    OFF "NOT ENABLE_SANITIZER_ADDRESS;NOT ENABLE_SANITIZER_THREAD;NOT ENABLE_SANITIZER_LEAK" OFF)

# examples
option(CPP_STARTER_USE_SML "Enable compilation of SML sample" OFF)
option(CPP_STARTER_USE_BOOST_BEAST "Enable compilation of boost beast sample" OFF)
option(CPP_STARTER_USE_CROW "Enable compilation of crow sample" OFF)
option(CPP_STARTER_USE_CPPZMQ_PROTO "Enable compilation of protobuf and cppzmq sample" OFF)
option(CPP_STARTER_USE_EMBEDDED_TOOLCHAIN "Enable compilation of an example cortex m4 project" OFF)
option(CPP_STARTER_USE_QT "Enable compilation of an example QT project" OFF)
option(CPP_STARTER_USE_OPEN62541PP "Enable compilation of an example open62541pp wrapper project" OFF)
option(CPP_STARTER_USE_OPEN62541 "Enable compilation of an example open62541 project" OFF)
option(CPP_STARTER_USE_SLINT "Enable compilation of an example slint project" OFF)
option(CPP_STARTER_USE_IMGUI "Enable compilation of an example imgui project" OFF)

# test frameworks
option(CPP_STARTER_USE_CATCH2 "Enable compilation of an example test project using catch2" ON)
option(CPP_STARTER_USE_GTEST "Enable compilation of an example test project using googletest" ON)

# ---------------------------------------------------------------------------
# Forward CMake feature flags to Conan so the cmake-conan develop2 provider
# installs exactly the packages needed.  CONAN_INSTALL_ARGS is read by
# conan_provide_dependency() on the first find_package() call (in src/).
# Without this, the conanfile.py default options are used, which leaves
# optional packages like ImGui uninstalled even when their CMake flag is ON.
# ---------------------------------------------------------------------------
foreach(_pair IN ITEMS
    "use_sml:CPP_STARTER_USE_SML"
    "use_boost_beast:CPP_STARTER_USE_BOOST_BEAST"
    "use_crow:CPP_STARTER_USE_CROW"
    "use_cppzmq_proto:CPP_STARTER_USE_CPPZMQ_PROTO"
    "use_qt:CPP_STARTER_USE_QT"
    "use_open62541:CPP_STARTER_USE_OPEN62541"
    "use_open62541pp:CPP_STARTER_USE_OPEN62541PP"
    "use_slint:CPP_STARTER_USE_SLINT"
    "use_imgui:CPP_STARTER_USE_IMGUI"
)
    string(REPLACE ":" ";" _pair_list "${_pair}")
    list(GET _pair_list 0 _conan_opt)
    list(GET _pair_list 1 _cmake_var)
    if(${_cmake_var})
        list(APPEND CONAN_INSTALL_ARGS "-o" "&:${_conan_opt}=True")
    else()
        list(APPEND CONAN_INSTALL_ARGS "-o" "&:${_conan_opt}=False")
    endif()
endforeach()
unset(_pair)
unset(_pair_list)
unset(_conan_opt)
unset(_cmake_var)
