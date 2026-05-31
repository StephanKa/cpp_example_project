find_package(Protobuf REQUIRED)
find_package(spdlog REQUIRED)
find_package(cppzmq REQUIRED)

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS proto/event.proto)

add_executable(test_cppzmq_proto_server server/main.cpp ${PROTO_SRCS} ${PROTO_HDRS})
add_executable(test_cppzmq_proto_client client/main.cpp ${PROTO_SRCS} ${PROTO_HDRS})

target_include_directories(test_cppzmq_proto_server PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/common ${CMAKE_CURRENT_BINARY_DIR})
target_include_directories(test_cppzmq_proto_client PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/common ${CMAKE_CURRENT_BINARY_DIR})

target_link_libraries(test_cppzmq_proto_server PRIVATE project_options project_warnings spdlog::spdlog_header_only cppzmq::cppzmq protobuf::protobuf)
target_link_libraries(test_cppzmq_proto_client PRIVATE project_options project_warnings spdlog::spdlog_header_only cppzmq::cppzmq protobuf::protobuf)
