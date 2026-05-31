set(TARGET test_arm_gcc)
find_package(fmt REQUIRED)

add_executable(${TARGET} main.cpp)
target_link_libraries(${TARGET} PRIVATE fmt::fmt-header-only)

set_target_properties(${TARGET} PROPERTIES SUFFIX ".elf")
target_link_options(${TARGET}
                    PRIVATE
                    -T${CMAKE_CURRENT_SOURCE_DIR}/linkerScript.ld
                    -Wl,-Map=${TARGET}.map
                    )
add_custom_target(${TARGET}.bin ALL
                  DEPENDS ${TARGET}
                  COMMAND ${CMAKE_OBJCOPY} -Obinary $<TARGET_FILE:${TARGET}> $<TARGET_FILE_DIR:${TARGET}>/$<TARGET_FILE_BASE_NAME:${TARGET}>.bin
                  COMMAND ${CMAKE_OBJCOPY} -Oihex $<TARGET_FILE:${TARGET}> $<TARGET_FILE_DIR:${TARGET}>/$<TARGET_FILE_BASE_NAME:${TARGET}>.hex
                  )
