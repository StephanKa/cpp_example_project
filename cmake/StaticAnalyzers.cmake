if(ENABLE_CPPCHECK)
    find_program(CPPCHECK cppcheck)
    if(CPPCHECK)
        set(CMAKE_CXX_CPPCHECK
            ${CPPCHECK}
            --suppress=missingInclude
            --enable=all
            --inline-suppr
            --inconclusive
            --std=c++${CMAKE_CXX_STANDARD}
            --check-level=exhaustive)
    else()
        message(SEND_ERROR "cppcheck requested but executable not found")
    endif()
endif()

if(ENABLE_CLANG_TIDY)
    find_program(CLANG_TIDY_BINARY clang-tidy)
    if(CLANG_TIDY_BINARY)
        set(_clang_tidy_args
            ${CLANG_TIDY_BINARY}
            --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy
            --header-filter=${CMAKE_SOURCE_DIR}/(src|test|fuzz_test)/.*
            -extra-arg=-Wno-unknown-warning-option
            -p=${CMAKE_BINARY_DIR}
        )
        if(WARNINGS_AS_ERRORS)
            list(APPEND _clang_tidy_args --warnings-as-errors=*)
        endif()
        set(CMAKE_CXX_CLANG_TIDY ${_clang_tidy_args})
        message(STATUS "clang-tidy enabled: ${CLANG_TIDY_BINARY}")
    else()
        message(SEND_ERROR "clang-tidy requested but executable not found")
    endif()
endif()

if(ENABLE_INCLUDE_WHAT_YOU_USE)
    find_program(INCLUDE_WHAT_YOU_USE include-what-you-use)
    if(INCLUDE_WHAT_YOU_USE)
        set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE ${INCLUDE_WHAT_YOU_USE})
    else()
        message(SEND_ERROR "include-what-you-use requested but executable not found")
    endif()
endif()
