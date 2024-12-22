import QtQuick
import QtQuick.Controls

// * The MaterialScrollBar class manages the scroll bar object.
ScrollBar
{

    // ! ----------------------------------------- ! //

    id: root
    active: true
    orientation: Qt.Vertical
    parent: parent
    anchors.top: parent.top
    anchors.left: parent.right
    anchors.bottom: parent.bottom
    anchors.rightMargin: 20

    contentItem: Rectangle
    {
        implicitWidth: 6
        implicitHeight: 100
        radius: width / 2
        color: root.pressed ? "#FF9800" : "#AAFF9800"
        opacity: (root.policy === ScrollBar.AlwaysOn) || ((root.active && root.size < 1.0) ? 0.75 : 0)

        // ? Animate the changes in opacity (default duration is 250 ms).

        Behavior on opacity { NumberAnimation {} }
    }
}