FIND_PACKAGE(open62541pp QUIET)
IF(NOT open62541pp_FOUND)
    MESSAGE("open62541pp could not be located in the CMake module search path. Downloading it from Git and building it locally")
    INCLUDE(FetchContent)
    FETCHCONTENT_DECLARE(
            open62541pp
            GIT_REPOSITORY https://github.com/open62541pp/open62541pp.git
            GIT_TAG v0.13.0
    )
    FETCHCONTENT_MAKEAVAILABLE(open62541pp)
ENDIF()

ADD_EXECUTABLE(open62541pp_client client.cpp)
TARGET_LINK_LIBRARIES(open62541pp_client PRIVATE open62541pp::open62541pp)

ADD_EXECUTABLE(open62541pp_server server.cpp)
TARGET_LINK_LIBRARIES(open62541pp_server PRIVATE open62541pp::open62541pp)
