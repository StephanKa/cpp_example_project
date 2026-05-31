find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick QuickControls2)

# Enable Qt's automatic tools for this directory
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

qt_add_executable(test_qt main.cpp)

# QML module: registers Backend (QML_ELEMENT) and bundles the .qml file
qt_add_qml_module(test_qt
    URI             qt_example
    VERSION         1.0
    QML_FILES       ui/main.qml
    SOURCES         Backend.h
)

target_link_libraries(test_qt PRIVATE
    project_options
    project_warnings
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
)

# Deploy Qt runtime next to the binary on Windows (requires windeployqt)
if(WIN32)
    add_custom_command(TARGET test_qt POST_BUILD
        COMMAND "${Qt6_DIR}/../../../bin/windeployqt.exe"
            --no-translations
            --qmldir "${CMAKE_CURRENT_SOURCE_DIR}/ui"
            "$<TARGET_FILE:test_qt>"
        COMMENT "Running windeployqt…"
    )
endif()
