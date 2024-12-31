import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../material"

// * The PageHeader class manages the page header.
Item
{
    // * Title.
    property string p_Title: ""

    // * Icon source file.
    property string p_Source: ""

    // ! ----------------------------------------- ! //

    id: root
    width: parent.width
    height: 50

    RowLayout
    {
        anchors.fill: parent
        spacing: 10

        Image
        {
            source: p_Source
            sourceSize.width: 32
            sourceSize.height: 32
            fillMode: Image.PreserveAspectFit
        }

        Text
        {
            text: p_Title
            color: "#93F9D8"
            font.pointSize: 20
            font.bold: true
            horizontalAlignment: Text.AlignLeft
        }

        Item
        {
            Layout.fillWidth: true
            Layout.fillHeight: true

            DragHandler
            {
                onActiveChanged: if (active) window.startSystemMove()
            }

            MouseArea
            {
                anchors.fill: parent
                onDoubleClicked: window.visibility === Window.Maximized ? window.showNormal() : window.showMaximized()
            }
        }

        MaterialIcon
        {
            source: "/svg/remove.svg"
            baseColor: "#FFFF00"

            function f_Click() { window.showMinimized() }
        }

        MaterialIcon
        {
            source: window.visibility === Window.Maximized ? "/svg/fullscreen_exit.svg" : "/svg/fullscreen.svg"
            baseColor: "#00FF00"

            function f_Click() { window.visibility === Window.Maximized ? window.showNormal() : window.showMaximized() }
        }

        MaterialIcon
        {
            source: "/svg/clear.svg"
            baseColor: "#FF0000"

            function f_Click() { _dialog_exit_.open() }
        }
    }
}