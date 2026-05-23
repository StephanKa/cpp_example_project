# SML
if(CMAKE_CROSSCOMPILING)
    if(CPP_STARTER_USE_EMBEDDED_TOOLCHAIN)
        message(STATUS "Using Embedded Toolchain")
        add_subdirectory(embedded)
    endif()
    return()
endif()

if(CPP_STARTER_USE_SML)
    message(STATUS "Using SML")
    add_subdirectory(sml)
endif()

# Boost Beast
if(CPP_STARTER_USE_BOOST_BEAST)
    message(STATUS "Using Boost Beast")
    add_subdirectory(boost.beast)
endif()

# Crow
if(CPP_STARTER_USE_CROW)
    message(STATUS "Using Crow")
    add_subdirectory(crow)
endif()

# CPPZMQ & Protobuf
if(CPP_STARTER_USE_CPPZMQ_PROTO)
    message(STATUS "Using CPPZMQ & Protobuf")
    add_subdirectory(protobuf.cppzmq)
endif()

# QT example
if(CPP_STARTER_USE_QT)
    message(STATUS "Using QT")
    add_subdirectory(qt)
endif()

# open62541pp example
if(CPP_STARTER_USE_OPEN62541PP)
    message(STATUS "Using open62541pp")
    add_subdirectory(open62541pp)
endif()

# open62541 example
if(CPP_STARTER_USE_OPEN62541)
    message(STATUS "Using open62541")
    add_subdirectory(open62541)
endif()

# slint example
if(CPP_STARTER_USE_SLINT)
    message(STATUS "Using slint")
    add_subdirectory(slint)
endif()

# imgui example
if(CPP_STARTER_USE_IMGUI)
    message(STATUS "Using imgui")
    add_subdirectory(imgui)
endif()

find_package(spdlog REQUIRED)
find_package(fmt REQUIRED)
# Generic test that uses conan libs
add_executable(intro main.cpp)
target_link_libraries(
        intro
        PRIVATE project_options
        project_warnings
        docopt_s
        fmt::fmt-header-only
        spdlog::spdlog_header_only)

target_include_directories(intro PRIVATE ${CMAKE_BINARY_DIR}/generated)
