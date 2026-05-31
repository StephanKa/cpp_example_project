find_package(GTest REQUIRED)

include(CTest)
include(GoogleTest)

add_executable(gtest_tests tests.cpp)
target_link_libraries(gtest_tests PRIVATE project_warnings project_options GTest::gtest_main)

# automatically discover tests that are defined in gtest based test files you can modify the unittests. Set TEST_PREFIX
# to whatever you want, or use different for different binaries
gtest_discover_tests(
        gtest_tests
        TEST_PREFIX
        "gtest_unittests."
        XML_OUTPUT_DIR
        .)

# Add a file containing a set of constexpr tests
add_executable(gtest_constexpr_tests constexpr_tests.cpp)
target_link_libraries(gtest_constexpr_tests PRIVATE project_options project_warnings GTest::gtest_main)

gtest_discover_tests(
        gtest_constexpr_tests
        TEST_PREFIX
        "gtest_constexpr."
        XML_OUTPUT_DIR
        .)
