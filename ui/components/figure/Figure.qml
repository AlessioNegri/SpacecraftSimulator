import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

import FigureCanvas 1.0

import "../material"

// * The Figure class manages the figure object.
Rectangle
{
    // * Object name for backend accessibility.
    property string p_ObjectName: ""

    // * Reference to model.
    property var r_Model: null

    // ! ----------------------------------------- ! //

    objectName: p_ObjectName + "Parent"
    color: "transparent"
    onWidthChanged: r_Model.resize_figure(width, height)
    onHeightChanged: r_Model.resize_figure(width, height)
    Component.onCompleted: r_Model.resize_figure(width, height)

    ToolBar
    {
        id: _tool_bar_
        height: 50
        width: r_Model.showCoord ? 600 : 210
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 10
        Material.primary: "#FFFFFF"

        background: Rectangle
        {
            color: "#209e9e9e"
            radius: 10
            border.color: Material.color(Material.Grey)
            border.width: 2
        }

        RowLayout
        {
            width: parent.width
            height: parent.height

            Item
            {
                width: 10
            }

            MaterialIcon
            {
                source: "/svg/home.svg"

                function f_Click() { r_Model.home() }
            }

            MaterialIcon
            {
                source: "/svg/arrow_back.svg"

                function f_Click() { r_Model.back() }
            }

            MaterialIcon
            {
                source: "/svg/arrow_forward.svg"

                function f_Click() { r_Model.forward() }
            }

            MaterialIcon
            {
                id: _pan_
                source: "/svg/pan_tool.svg"
                checkable: true

                function f_Click()
                {
                    _pan_.checked = !_pan_.checked

                    if (_zoom_.checked) _zoom_.checked = false

                    r_Model.pan()
                }
            }

            MaterialIcon
            {
                id: _zoom_
                source: "/svg/zoom_in.svg"
                checkable: true

                function f_Click()
                {
                    _zoom_.checked = !_zoom_.checked

                    if (_pan_.checked) _pan_.checked = false

                    r_Model.zoom()
                }
            }

            Item { Layout.fillWidth: true }

            TextInput
            {
                text: "(x, y) = " + r_Model.coord
                color: "#FFFFFF"
                font.pointSize: 12
                font.bold: true
                readOnly: true
                visible: r_Model.showCoord
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