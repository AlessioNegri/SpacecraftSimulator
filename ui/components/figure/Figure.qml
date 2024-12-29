import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

import FigureCanvas 1.0

import "../material"

// * The Figure class manages the figure object.
Rectangle
{
    // * True if the figure is expanded.
    property bool p_Expanded: false

    // * Object name for backend accessibility.
    property string p_ObjectName: ""

    // * Reference to model.
    property var r_Model: null

    // * Reference to original parent.
    property var r_OriginalParent: null

    // * Reference to expanded parent.
    property var r_ExpandedParent: null

    // ! ----------------------------------------- ! //

    objectName: p_ObjectName + "Parent"
    id: figure
    height: 450
    color: "#162A35"
    radius: 10
    border.width: 2
    border.color: Material.color(Material.Grey)
    onWidthChanged: if (r_Model !== null) r_Model.resize_figure(width, height)
    onHeightChanged: if (r_Model !== null) r_Model.resize_figure(width, height)
    Component.onCompleted: if (r_Model !== null) r_Model.resize_figure(width, height)

    states:
    [
        State
        {
            name: "expand"
            
            ParentChange
            {
                target: figure
                parent: r_ExpandedParent
            }
        },
        State
        {
            name: "collapse"
            
            ParentChange
            {
                target: figure
                parent: r_OriginalParent
            }
        }
    ]

    ToolBar
    {
        id: _tool_bar_
        height: 50
        z: 2
        //width: r_Model === null ? 0 : (r_Model.showCoord ? 600 : 210)
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        //anchors.horizontalCenter: parent.horizontalCenter
        anchors.leftMargin: 10
        anchors.topMargin: 10
        anchors.rightMargin: 10
        Material.primary: "#FFFFFF"

        background: Rectangle
        {
            color: "transparent" //"#162A35"
            /*radius: 10
            border.color: Material.color(Material.Grey)
            border.width: 2*/
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
                sourceSize.width: 24
                sourceSize.height: 24

                function f_Click() { r_Model.home() }
            }

            MaterialIcon
            {
                source: "/svg/arrow_back.svg"
                sourceSize.width: 24
                sourceSize.height: 24

                function f_Click() { r_Model.back() }
            }

            MaterialIcon
            {
                source: "/svg/arrow_forward.svg"
                sourceSize.width: 24
                sourceSize.height: 24

                function f_Click() { r_Model.forward() }
            }

            MaterialIcon
            {
                id: _pan_
                source: "/svg/pan_tool.svg"
                sourceSize.width: 24
                sourceSize.height: 24
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
                sourceSize.width: 24
                sourceSize.height: 24
                checkable: true

                function f_Click()
                {
                    _zoom_.checked = !_zoom_.checked

                    if (_pan_.checked) _pan_.checked = false

                    r_Model.zoom()
                }
            }

            MaterialIcon
            {
                source: p_Expanded ? "/svg/fullscreen_exit.svg" : "/svg/fullscreen.svg"
                sourceSize.width: 24
                sourceSize.height: 24
                visible: r_OriginalParent !== null && r_ExpandedParent != null

                function f_Click()
                {
                    p_Expanded = !p_Expanded

                    figure.state = p_Expanded ? "expand" : "collapse"
                }
            }

            Item { Layout.fillWidth: true }

            TextInput
            {
                text: "(x, y) = " + (r_Model !== null ? r_Model.coord : "")
                color: "#FFFFFF"
                font.pointSize: 12
                font.bold: true
                readOnly: true
                visible: (r_Model !== null ? r_Model.showCoord : false)
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
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        anchors.rightMargin: 5
        height: parent.height - _tool_bar_.height - 10
    }
}