function(setup_multi_config)
    get_property(BUILDING_MULTI_CONFIG GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)
    if(BUILDING_MULTI_CONFIG)
        if(NOT CMAKE_BUILD_TYPE)
            # Make sure that all supported configuration types have their
            # associated conan packages available. You can reduce this
            # list to only the configuration types you use, but only if one
            # is not forced-set on the command line for VS
            message(TRACE "Setting up multi-config build types")
            set(CMAKE_CONFIGURATION_TYPES
                Debug
                Release
                RelWithDebInfo
                MinSizeRel
                CACHE STRING "Enabled build types" FORCE)
        else()
            message(TRACE "User chose a specific build type, so we are using that")
            set(CMAKE_CONFIGURATION_TYPES
                ${CMAKE_BUILD_TYPE}
                CACHE STRING "Enabled build types" FORCE)
        endif()
    endif()
endfunction()
