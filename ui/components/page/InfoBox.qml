import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../material"

// * The InfoBox class manages the info box object in home page.
Rectangle
{
    // * Info box image source.
    property string p_Image: ""

    // * Info box icon source.
    property string p_Icon: ""

    // * Info box text.
    property string p_Text: ""
    
    // * Index of the page.
    property int p_PageIndex: 0

    // * Link to the page.
    property string p_PageLink: ""

    // ! ----------------------------------------- ! //

    color: "#C0162A35"
    radius: 10
    Layout.fillWidth: true
    Layout.fillHeight: true

    Image
    {
        source: p_Image
        anchors.fill: parent
        anchors.rightMargin: parent.width / 2
        anchors.leftMargin: 5
        anchors.topMargin: 5
        anchors.bottomMargin: 5

        Rectangle
        {
            color: "#162A35"
            width: 2
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
        }
    }

    Rectangle
    {
        color: "transparent"
        radius: 10
        border.width: 3
        border.color: "#162A35"
        anchors.fill: parent
        anchors.rightMargin: parent.width / 2
        anchors.leftMargin: 5
        anchors.topMargin: 5
        anchors.bottomMargin: 5
    }

    Rectangle
    {
        color: "transparent"
        radius: 7
        border.width: 5
        border.color: "#162A35"
        anchors.fill: parent
        anchors.rightMargin: parent.width / 2
        anchors.leftMargin: 3
        anchors.topMargin: 3
        anchors.bottomMargin: 3
    }
    
    ColumnLayout
    {
        anchors.fill: parent
        anchors.leftMargin: parent.width / 2

        Text
        {
            text: p_Text
            color: "#FFFFFF"
            font.pixelSize: parent.height / 5
            font.bold: true
            Layout.alignment: Qt.AlignCenter
        }

        MaterialIcon
        {
            source: p_Icon
            sourceSize.width: parent.height / 2
            sourceSize.height: parent.height / 2
            baseColor: "transparent"
            hoverColor: "transparent"
            Layout.alignment: Qt.AlignCenter
        }
    }

    Rectangle
    {
        color: "transparent"
        radius: 5
        anchors.fill: parent
        border.width: 2
        border.color: "#FFFFFF"
        visible: _mouse_area_.containsMouse
    }

    MouseArea
    {
        id: _mouse_area_
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: { gp_CurrentPage = p_PageIndex; loader.source = p_PageLink }
    }
}