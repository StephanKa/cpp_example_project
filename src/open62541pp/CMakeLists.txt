find_package(open62541pp QUIET)
if(NOT open62541pp_FOUND)
    message(STATUS "open62541pp could not be located in the CMake module search path. Downloading it from Git and building it locally")
    include(FetchContent)
    FetchContent_Declare(
            open62541pp
            GIT_REPOSITORY https://github.com/open62541pp/open62541pp.git
            GIT_TAG v0.13.0
    )
    FetchContent_MakeAvailable(open62541pp)
endif()

add_executable(open62541pp_client client.cpp)
target_link_libraries(open62541pp_client PRIVATE project_options project_warnings open62541pp::open62541pp)

add_executable(open62541pp_server server.cpp)
target_link_libraries(open62541pp_server PRIVATE project_options project_warnings open62541pp::open62541pp)
