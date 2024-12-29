import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// * The Stage class manages the stage component.
Rectangle
{
    // * True if selected.
    property bool p_Selected: false

    // * True if in use.
    property bool p_InUse: false

    // * Image source file.
    property string p_Source: ""

    // * Stage text.
    property string p_Text: ""

    // * Override to implement the "Click" action.
    function f_Click() {}

    // ! ----------------------------------------- ! //

    Layout.fillWidth: true
    Layout.fillHeight: true
    color: "transparent"
    radius: 10
    border.width: p_Selected ? 2 : 0
    border.color: "#FFFFFF"

    Image
    {
        source: p_Source
        sourceSize.height: parent.height
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: parent
        anchors.margins: 10
        opacity: p_Selected ? 1.0 : 0.5
    }

    Rectangle
    {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 10
        width: 80
        height: 40
        color: p_InUse ? "#804CAF50" : "#80F44336"
        radius: 10
        border.width: 2
        border.color: "#FFFFFF"
        opacity: p_Selected ? 1.0 : 0.5

        Text
        {
            text: p_InUse ? "ON" : "OFF"
            color: "#FFFFFF"
            font.bold: true
            font.pointSize: 12
            anchors.centerIn: parent
        }
    }

    Rectangle
    {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 10
        width: 80
        height: 40
        color: "#80ff9800"
        radius: 10
        border.width: 2
        border.color: "#FFFFFF"
        opacity: p_Selected ? 1.0 : 0.5

        Text
        {
            text: p_Text
            color: "#FFFFFF"
            font.bold: true
            font.pointSize: 12
            anchors.centerIn: parent
        }
    }

    MouseArea
    {
        id: _mouse_area_
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true
        onClicked: f_Click()
    }
}