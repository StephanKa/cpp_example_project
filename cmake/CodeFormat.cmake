# To exclude directories from the format check, add corresponding clang-format config files into those directories.
find_program(CLANG_FORMAT_BINARY NAMES clang-format)
find_program(CLANG_TIDY_BINARY   NAMES clang-tidy)

if(CLANG_FORMAT_BINARY)
    add_custom_target(clang-format-check
                      USES_TERMINAL
                      COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/scripts/run-clang-format.py
                              -clang-format-binary ${CLANG_FORMAT_BINARY}
                              -warnings-as-errors
                      )

    add_custom_target(clang-format-fix
                      USES_TERMINAL
                      COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/scripts/run-clang-format.py
                              -clang-format-binary ${CLANG_FORMAT_BINARY}
                              -fix
                      )
else()
    message(WARNING "clang-format not found — clang-format-check and clang-format-fix targets are unavailable")
endif()

if(CLANG_TIDY_BINARY)
    add_custom_target(clang-tidy-check
                      USES_TERMINAL
                      WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
                      COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/scripts/run-clang-tidy.py
                              -clang-tidy-binary ${CLANG_TIDY_BINARY}
                              -p ${CMAKE_BINARY_DIR}
    )

    add_custom_target(clang-tidy-diff-check
                      USES_TERMINAL
                      WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
                      COMMAND git diff -U0 HEAD --no-prefix | ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/scripts/run-clang-tidy-diff.py
                              -clang-tidy-binary ${CLANG_TIDY_BINARY}
                              -path ${CMAKE_BINARY_DIR}
    )
else()
    message(WARNING "clang-tidy not found — clang-tidy-check and clang-tidy-diff-check targets are unavailable")
endif()
