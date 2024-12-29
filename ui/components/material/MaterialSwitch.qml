import QtQuick
import QtQuick.Controls.Basic

// * The MaterialSwitch class manages the switch object.
Switch
{
    id: root
    text: ""
    font.pointSize: 12
    font.bold: true

    indicator: Rectangle
    {
        implicitWidth: 50
        implicitHeight: 26
        x: root.leftPadding
        y: parent.height / 2 - height / 2
        radius: 10
        color: root.checked ? "#FF9800" : "#ffffff"
        border.color: root.checked ? "#FF9800" : "#cccccc"

        Rectangle
        {
            x: root.checked ? parent.width - width : 0
            width: 20
            height: 20
            radius: width / 2
            color: root.down ? "#cccccc" : "#ffffff"
            border.color: root.checked ? (root.down ? "#FF5722" : "#FF9800") : "#999999"
        }
    }

    contentItem: Text
    {
        text: root.text
        font: root.font
        opacity: enabled ? 1.0 : 0.3
        color: root.down ? "#ffffff" : "#ffffff"
        verticalAlignment: Text.AlignVCenter
        leftPadding: root.indicator.width + root.spacing
    }
}