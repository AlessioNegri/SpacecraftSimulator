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
    anchors.fill: parent
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
                icon.source: "/images/img/home.svg"
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked: r_Model.home()
            }

            Button
            {
                icon.source: "/images/img/arrow_back.svg"
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter
                onClicked: r_Model.back()
            }

            Button
            {
                icon.source: "/images/img/arrow_forward.svg"
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter
                onClicked: r_Model.forward()
            }

            Button
            {
                id: _departure_pan_
                checkable: true
                icon.source: "/images/img/pan_tool.svg"
                Material.background: _departure_pan_.checked ? Material.DeepOrange : Material.Indigo
                Material.foreground: "#FFFFFF"
                Material.accent: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter
                
                onClicked:
                {
                    if (_departure_zoom_.checked) _departure_zoom_.checked = false

                    r_Model.pan()
                }
            }

            Button
            {
                id: _departure_zoom_
                checkable: true
                icon.source: "/images/img/zoom_in.svg"
                Material.background: _departure_zoom_.checked ? Material.DeepOrange : Material.Indigo
                Material.foreground: "#FFFFFF"
                Material.accent: "#FFFFFF"
                Layout.alignment: Qt.AlignHCenter

                onClicked:
                {
                    if (_departure_pan_.checked) _departure_pan_.checked = false

                    r_Model.zoom()
                }
            }

            Item { Layout.fillWidth: true }

            TextInput
            {
                text: r_Model.coord
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