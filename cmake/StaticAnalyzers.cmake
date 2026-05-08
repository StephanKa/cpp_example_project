IF(ENABLE_CPPCHECK)
    FIND_PROGRAM(CPPCHECK cppcheck)
    IF(CPPCHECK)
        SET(CMAKE_CXX_CPPCHECK
            ${CPPCHECK}
            --suppress=missingInclude
            --enable=all
            --inline-suppr
            --inconclusive)
    ELSE()
        MESSAGE(SEND_ERROR "cppcheck requested but executable not found")
    ENDIF()
ENDIF()

IF(ENABLE_CLANG_TIDY)
    FIND_PROGRAM(CLANG_TIDY_BINARY clang-tidy)
    IF(CLANG_TIDY_BINARY)
        SET(_clang_tidy_args
            ${CLANG_TIDY_BINARY}
            --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy
            --header-filter=${CMAKE_SOURCE_DIR}/(src|test|fuzz_test)/.*
            -extra-arg=-Wno-unknown-warning-option
            -p=${CMAKE_BINARY_DIR}
        )
        IF(WARNINGS_AS_ERRORS)
            LIST(APPEND _clang_tidy_args --warnings-as-errors=*)
        ENDIF()
        SET(CMAKE_CXX_CLANG_TIDY ${_clang_tidy_args})
        MESSAGE(STATUS "clang-tidy enabled: ${CLANG_TIDY_BINARY}")
    ELSE()
        MESSAGE(SEND_ERROR "clang-tidy requested but executable not found")
    ENDIF()
ENDIF()

IF(ENABLE_INCLUDE_WHAT_YOU_USE)
    FIND_PROGRAM(INCLUDE_WHAT_YOU_USE include-what-you-use)
    IF(INCLUDE_WHAT_YOU_USE)
        SET(CMAKE_CXX_INCLUDE_WHAT_YOU_USE ${INCLUDE_WHAT_YOU_USE})
    ELSE()
        MESSAGE(SEND_ERROR "include-what-you-use requested but executable not found")
    ENDIF()
ENDIF()
