find_package(Catch2 REQUIRED)

include(CTest)
include(Catch)

add_executable(catch_tests tests.cpp)
target_link_libraries(catch_tests PRIVATE project_warnings project_options Catch2::Catch2WithMain)

# automatically discover tests that are defined in catch based test files you can modify the unittests. Set TEST_PREFIX
# to whatever you want, or use different for different binaries
catch_discover_tests(
        catch_tests
        TEST_PREFIX
        "catch_unittests."
        REPORTER
        JUnit
        OUTPUT_DIR
        .
        OUTPUT_PREFIX
        "catch_unittests."
        OUTPUT_SUFFIX
        .xml)

# Add a file containing a set of constexpr tests
add_executable(catch_constexpr_tests constexpr_tests.cpp)
target_link_libraries(catch_constexpr_tests PRIVATE project_options project_warnings Catch2::Catch2WithMain)

catch_discover_tests(
        catch_constexpr_tests
        TEST_PREFIX
        "catch_constexpr."
        REPORTER
        JUnit
        OUTPUT_DIR
        .
        OUTPUT_PREFIX
        "catch_constexpr."
        OUTPUT_SUFFIX
        .xml)

# Disable the constexpr portion of the test, and build again this allows us to have an executable that we can debug when
# things go wrong with the constexpr testing
add_executable(catch_relaxed_constexpr_tests constexpr_tests.cpp)
target_link_libraries(catch_relaxed_constexpr_tests PRIVATE project_options project_warnings Catch2::Catch2WithMain)
target_compile_definitions(catch_relaxed_constexpr_tests PRIVATE -DCATCH_CONFIG_RUNTIME_STATIC_REQUIRE)

catch_discover_tests(
        catch_relaxed_constexpr_tests
        TEST_PREFIX
        "catch_relaxed_constexpr."
        REPORTER
        JUnit
        OUTPUT_DIR
        .
        OUTPUT_PREFIX
        "catch_relaxed_constexpr."
        OUTPUT_SUFFIX
        .xml)
