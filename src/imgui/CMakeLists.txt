find_package(ImGui REQUIRED)
find_package(ImPlot REQUIRED)
find_package(glfw3 REQUIRED)
find_package(OpenGL REQUIRED)

# Retrieve the imgui package include directory.
# Conan's CMakeDeps sets INTERFACE_INCLUDE_DIRECTORIES to a real path at configure time,
# so get_target_property works here without config-specific suffixes like _DEBUG/_RELEASE.
get_target_property(_imgui_incdirs imgui::imgui INTERFACE_INCLUDE_DIRECTORIES)
list(GET _imgui_incdirs 0 IMGUI_INCLUDE_DIR)

# Backend sources were copied from res/bindings -> include/backends by conanfile.py generate()
add_executable(test_imgui
    main.cpp
    ${IMGUI_INCLUDE_DIR}/backends/imgui_impl_glfw.cpp
    ${IMGUI_INCLUDE_DIR}/backends/imgui_impl_opengl3.cpp
)

target_link_libraries(test_imgui PRIVATE
    project_options
    project_warnings
    imgui::imgui
    implot::implot
    glfw
    OpenGL::GL
)

# On Windows, copy runtime DLLs next to the binary
if(WIN32)
    add_custom_command(TARGET test_imgui POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            $<TARGET_RUNTIME_DLLS:test_imgui>
            $<TARGET_FILE_DIR:test_imgui>
        COMMAND_EXPAND_LISTS
    )
endif()
