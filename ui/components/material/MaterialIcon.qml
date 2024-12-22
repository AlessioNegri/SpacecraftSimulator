import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

// * The MaterialIcon class manages the icon object.
Image
{
    // * True for a checkable icon
    property bool checkable: false

    // * Checked state
    property bool checked: false

    // * Hover color
    property color hoverColor: "#FFFFFF"

    // * Color
    property color baseColor: "#AAFFFFFF"

    // * Override to implement the "Click" action.
    function f_Click() {}

    // ! ----------------------------------------- ! //

    sourceSize.width: 32
    sourceSize.height: 32
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

    ColorOverlay
    {
        anchors.fill: parent
        source: parent
        color: _mouse_area_icon_.containsMouse ? hoverColor : (checked ? "red" : baseColor)
    }

    MouseArea
    {
        id: _mouse_area_icon_
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true
        onClicked: f_Click()
    }
}