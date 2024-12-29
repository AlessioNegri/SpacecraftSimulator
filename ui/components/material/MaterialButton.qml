import QtQuick
import QtQuick.Controls.Basic

// * The MaterialButton class manages the button object.
Button
{
    id: root
    text: ""
    font.pointSize: 10
    font.bold: true
    hoverEnabled: true

    contentItem: Text
    {
        text: root.text
        font: root.font
        opacity: enabled ? 1.0 : 0.3
        color: root.down ? "#80FFFFFF" : "#FFFFFF"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle
    {
        implicitWidth: 100
        implicitHeight: 20
        opacity: enabled ? 1 : 0.3
        color: root.hovered ? "#487D76" : (checked ? "#80F44336" : "#162A35")
        border.color: root.down ? "#487D76" : (checked ? "#F44336" : "#93F9D8")
        border.width: 2
        radius: 10
    }
}