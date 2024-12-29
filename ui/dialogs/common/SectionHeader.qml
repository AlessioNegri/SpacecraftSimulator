import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

// * The SectionHeader class manages the header on each section of the selected left item.
Rectangle
{
    // * Section header title.
    property string p_Title: ""

    // * Section header source icon.
    property string p_Icon: ""

    // * Section header hide.
    property bool p_Hide: false

    // * Color.
    property color p_Color: "#93F9D8"

    // ! ----------------------------------------- ! //

    color: "transparent"
    height: _layout_.height + 20
    Layout.fillWidth: true

    Rectangle
    {
        anchors.fill: parent
        radius: 5
        color: p_Color
        opacity: 0.25
    }

    Rectangle
    {
        width: 3
        height: _layout_.height + 20
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        radius: 20
        color: p_Color
    }

    MouseArea
    {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true
        onClicked: p_Hide = !p_Hide
    }

    RowLayout
    {
        id: _layout_
        spacing: 20
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 10

        Rectangle
        {
            width: 54
            height: 54
            color: "#B0BEC5"//"#4093F9D8"
            radius: width / 2
            border.width: 3
            border.color: p_Color
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Image
            {
                source: p_Icon
                sourceSize.width: 40
                sourceSize.height: 40
                anchors.centerIn: parent
            }
        }

        Text
        {
            text: p_Title
            color: p_Color
            font.pointSize: 14
            font.bold: true
            verticalAlignment: Text.AlignVCenter
        }

        Image
        {
            source: p_Hide ? "/svg/arrow_drop_down.svg" : "/svg/arrow_drop_up.svg"
            sourceSize.width: 40
            sourceSize.height: 40
            Layout.alignment: Qt.AlignVCenter

            ColorOverlay
            {
                anchors.fill: parent
                source: parent
                color: p_Color
            }
        }
    }
}