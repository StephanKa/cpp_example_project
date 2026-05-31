find_package(open62541 REQUIRED)

add_executable(open62541_client client.cpp)
target_link_libraries(open62541_client PRIVATE project_options project_warnings open62541::open62541)

add_executable(open62541_server server.cpp)
target_link_libraries(open62541_server PRIVATE project_options project_warnings open62541::open62541)
