FIND_PACKAGE(ImGui REQUIRED)
FIND_PACKAGE(ImPlot REQUIRED)
FIND_PACKAGE(glfw3 REQUIRED)
FIND_PACKAGE(OpenGL REQUIRED)

# Retrieve the imgui package include directory.
# Conan's CMakeDeps sets INTERFACE_INCLUDE_DIRECTORIES to a real path at configure time,
# so GET_TARGET_PROPERTY works here without config-specific suffixes like _DEBUG/_RELEASE.
GET_TARGET_PROPERTY(_imgui_incdirs imgui::imgui INTERFACE_INCLUDE_DIRECTORIES)
LIST(GET _imgui_incdirs 0 IMGUI_INCLUDE_DIR)

# Backend sources were copied from res/bindings -> include/backends by conanfile.py generate()
ADD_EXECUTABLE(test_imgui
    main.cpp
    ${IMGUI_INCLUDE_DIR}/backends/imgui_impl_glfw.cpp
    ${IMGUI_INCLUDE_DIR}/backends/imgui_impl_opengl3.cpp
)

TARGET_LINK_LIBRARIES(test_imgui PRIVATE
    imgui::imgui
    implot::implot
    glfw
    OpenGL::GL
)

# On Windows and Linux, copy runtime DLLs/SOs next to the binary
IF(WIN32)
    ADD_CUSTOM_COMMAND(TARGET test_imgui POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            $<TARGET_RUNTIME_DLLS:test_imgui>
            $<TARGET_FILE_DIR:test_imgui>
        COMMAND_EXPAND_LISTS
    )
ENDIF()
