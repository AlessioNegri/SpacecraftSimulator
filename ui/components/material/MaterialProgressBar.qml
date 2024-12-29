import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// * The MaterialProgressBar class manages the progress bar object.
ProgressBar
{
    // ! ----------------------------------------- ! //

    id: root
    value: 0
    implicitWidth: 200
    implicitHeight: 32

    background: Rectangle
    {
        implicitWidth: 200
        implicitHeight: 35
        radius: 3
        color: "#487D76"
    }

    contentItem: Item
    {
        implicitWidth: 200
        implicitHeight: 30

        Rectangle
        {
            width: root.visualPosition * parent.width
            height: parent.height
            radius: 2
            color: "#8093F9D8"
        }

        Text
        {
            text: parseInt(root.value * 100) + " %"
            anchors.centerIn: parent
            font.bold: true
            font.pointSize: 12
            color: "#FFFFFF"
        }
    }
}