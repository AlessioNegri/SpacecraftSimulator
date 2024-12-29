import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

// * The MaterialIcon class manages the icon object.
Image
{
    // * True for a selectable icon.
    property bool selectable: false

    // * True for a checkable icon.
    property bool checkable: false

    // * Checked state.
    property bool checked: false

    // * Tooltip location.
    property int tooltipLocation: Qt.AlignRight

    // * Hover color.
    property color hoverColor: "#93F9D8"

    // * Color.
    property color baseColor: "#487D76"

    // * Tooltip text.
    property string tooltip: ""

    // * Override to implement the "Click" action.
    function f_Click() {}

    // ! ----------------------------------------- ! //

    id: root
    sourceSize.width: 32
    sourceSize.height: 32
    fillMode: Image.PreserveAspectFit
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

    ColorOverlay
    {
        anchors.fill: parent
        source: parent
        color: _mouse_area_icon_.containsMouse ? hoverColor : (checkable && checked ? "#FFEB3B" : baseColor)
    }

    MouseArea
    {
        id: _mouse_area_icon_
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true
        onClicked: f_Click()
    }

    ToolTip
    {
        parent: root
        visible: tooltip !== "" && _mouse_area_icon_.containsMouse
        text: tooltip
        x: tooltipLocation === Qt.AlignRight ? (root.width + 15) : (root.width / 2 - width / 2)
        y: tooltipLocation === Qt.AlignRight ? (root.height / 2 - height / 2) : (- height - 15)
        delay: 0
        timeout: 0
        font.bold: true
        exit: Transition {}
        
        background: Rectangle
        {
            color: "#487D76"
            radius: 5
        }
    }

    Rectangle
    {
        anchors.centerIn: parent
        width: parent.width * 1.25
        height: parent.height * 1.25
        radius: 10
        border.width: 2
        border.color: "#93F9D8"
        color: "#11487D76"
        visible: selectable && checked
    }
}