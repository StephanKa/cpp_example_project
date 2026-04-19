FIND_PACKAGE(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick QuickControls2)

# Enable Qt's automatic tools for this directory
SET(CMAKE_AUTOMOC ON)
SET(CMAKE_AUTORCC ON)

QT_ADD_EXECUTABLE(test_qt main.cpp)

# QML module: registers Backend (QML_ELEMENT) and bundles the .qml file
QT_ADD_QML_MODULE(test_qt
    URI             qt_example
    VERSION         1.0
    QML_FILES       ui/main.qml
    SOURCES         Backend.h
)

TARGET_LINK_LIBRARIES(test_qt PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
)

# Deploy Qt runtime next to the binary on Windows (requires windeployqt)
IF(WIN32)
    ADD_CUSTOM_COMMAND(TARGET test_qt POST_BUILD
        COMMAND "${Qt6_DIR}/../../../bin/windeployqt.exe"
            --no-translations
            --qmldir "${CMAKE_CURRENT_SOURCE_DIR}/ui"
            "$<TARGET_FILE:test_qt>"
        COMMENT "Running windeployqt…"
    )
ENDIF()
