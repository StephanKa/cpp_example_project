import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import qt_example

ApplicationWindow {
    id: root
    visible: true
    width: 480
    height: 320
    title: qsTr("Qt QML Timer Example")

    Backend {
        id: backend
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 24

        // ---------- Timer display ----------
        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Elapsed: %1 s").arg(backend.elapsedSeconds)
            font.pixelSize: 36
            font.bold: true
        }

        // ---------- Status text ----------
        Label {
            Layout.alignment: Qt.AlignHCenter
            text: backend.running ? qsTr("Timer running…") : qsTr("Timer stopped")
            color: backend.running ? "#2ecc71" : "#e74c3c"
            font.pixelSize: 16
        }

        // ---------- Buttons ----------
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 12

            Button {
                text: qsTr("Start")
                enabled: !backend.running
                onClicked: backend.start()
            }

            Button {
                text: qsTr("Stop")
                enabled: backend.running
                onClicked: backend.stop()
            }

            Button {
                text: qsTr("Reset")
                onClicked: backend.reset()
            }
        }
    }
}
