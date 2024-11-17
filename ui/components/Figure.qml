import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import FigureCanvas 1.0

// ? The Figure class manages the figure object.
Rectangle
{
    // ? Object name for backend accessibility.
    property string p_ObjectName: ""

    // ? Reference to model.
    property var r_Model: null

    // !-----------------------------------------! //

    objectName: p_ObjectName + "Parent"
    //anchors.fill: parent
    color: "transparent"
    //radius: 5
    //border.width: 2
    //border.color: Material.color(Material.Indigo)
    onWidthChanged: r_Model.resize_figure(width, height)
    onHeightChanged: r_Model.resize_figure(width, height)
    Component.onCompleted: r_Model.resize_figure(width, height)

    ToolBar
    {
        id: _tool_bar_
        height: 50
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 10
        Material.primary: "#FFFFFF"
        background: Rectangle { color: "transparent" }

        RowLayout
        {
            width: parent.width
            height: parent.height

            Item { width: 10 }

            Button
            {
                text: "Restore"
                icon.source: "/svg/home.svg"
                Material.background: "#FF5722"
                Material.foreground: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked: r_Model.home()

                HoverHandler
                {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                    cursorShape: Qt.PointingHandCursor
                }
            }

            Button
            {
                text: "Back"
                icon.source: "/svg/arrow_back.svg"
                Material.background: "#FF5722"
                Material.foreground: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter
                onClicked: r_Model.back()

                HoverHandler
                {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                    cursorShape: Qt.PointingHandCursor
                }
            }

            Button
            {
                text: "Next"
                icon.source: "/svg/arrow_forward.svg"
                Material.background: "#FF5722"
                Material.foreground: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter
                onClicked: r_Model.forward()

                HoverHandler
                {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                    cursorShape: Qt.PointingHandCursor
                }
            }

            Button
            {
                id: _departure_pan_
                checkable: true
                text: "Pan"
                icon.source: "/svg/pan_tool.svg"
                Material.background: _departure_pan_.checked ? "#3F51B5" : "#FF5722"
                Material.foreground: "#FFFFFF"
                Material.accent: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter
                
                onClicked:
                {
                    if (_departure_zoom_.checked) _departure_zoom_.checked = false

                    r_Model.pan()
                }

                HoverHandler
                {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                    cursorShape: Qt.PointingHandCursor
                }
            }

            Button
            {
                id: _departure_zoom_
                checkable: true
                text: "Zoom"
                icon.source: "/svg/zoom_in.svg"
                Material.background: _departure_zoom_.checked ? "#3F51B5" : "#FF5722"
                Material.foreground: "#FFFFFF"
                Material.accent: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter

                onClicked:
                {
                    if (_departure_pan_.checked) _departure_pan_.checked = false

                    r_Model.zoom()
                }

                HoverHandler
                {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                    cursorShape: Qt.PointingHandCursor
                }
            }

            Item { Layout.fillWidth: true }

            TextInput
            {
                text: "Coordinates: " + r_Model.coord
                color: "#FFFFFF"
                font.pointSize: 12
                font.bold: true
                readOnly: true
            }

            Item { width: 10 }
        }
    }

    FigureCanvas
    {
        objectName: p_ObjectName
        dpi_ratio: Screen.devicePixelRatio
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 10
        height: parent.height - _tool_bar_.height - 20
    }
}