function(enable_sanitizers project_name)

    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES ".*Clang")

        if(ENABLE_COVERAGE)
            target_compile_options(${project_name} INTERFACE
                $<$<COMPILE_LANGUAGE:CXX>:--coverage>
                $<$<COMPILE_LANGUAGE:CXX>:-O0>
                $<$<COMPILE_LANGUAGE:CXX>:-g>)
            target_link_libraries(${project_name} INTERFACE --coverage)
        endif()

        set(SANITIZERS "")

        if(ENABLE_SANITIZER_ADDRESS)
            list(APPEND SANITIZERS "address")
        endif()

        if(ENABLE_SANITIZER_LEAK)
            list(APPEND SANITIZERS "leak")
        endif()

        if(ENABLE_SANITIZER_UNDEFINED_BEHAVIOR)
            list(APPEND SANITIZERS "undefined")
        endif()

        if(ENABLE_SANITIZER_THREAD)
            if("address" IN_LIST SANITIZERS OR "leak" IN_LIST SANITIZERS)
                message(WARNING "Thread sanitizer does not work with Address and Leak sanitizer enabled")
            else()
                list(APPEND SANITIZERS "thread")
            endif()
        endif()

        if(ENABLE_SANITIZER_MEMORY AND CMAKE_CXX_COMPILER_ID MATCHES ".*Clang")
            if("address" IN_LIST SANITIZERS
               OR "thread" IN_LIST SANITIZERS
               OR "leak" IN_LIST SANITIZERS)
                message(WARNING "Memory sanitizer does not work with Address, Thread and Leak sanitizer enabled")
            else()
                list(APPEND SANITIZERS "memory")
            endif()
        endif()

        list(JOIN SANITIZERS "," LIST_OF_SANITIZERS)

        if(LIST_OF_SANITIZERS)
            target_compile_options(${project_name} INTERFACE
                -fsanitize=${LIST_OF_SANITIZERS}
                -fno-omit-frame-pointer)
            target_link_options(${project_name} INTERFACE -fsanitize=${LIST_OF_SANITIZERS})
        endif()

    elseif(MSVC)

        if(ENABLE_SANITIZER_ADDRESS)
            message(STATUS "Enabling MSVC AddressSanitizer (/fsanitize=address)")
            target_compile_options(${project_name} INTERFACE /fsanitize=address)
            target_link_options(${project_name} INTERFACE /INCREMENTAL:NO)
        endif()
        if(ENABLE_SANITIZER_LEAK OR ENABLE_SANITIZER_UNDEFINED_BEHAVIOR OR
           ENABLE_SANITIZER_THREAD OR ENABLE_SANITIZER_MEMORY)
            message(WARNING "MSVC only supports AddressSanitizer; other sanitizer options are ignored.")
        endif()

    endif()

endfunction()
