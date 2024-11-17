import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

// ? The PageInterplanetaryTransfer class manages the interplanetary transfer page.
Page
{
    background: Rectangle { color: "#424242" }

    header: Rectangle
    {
        id: _header_
        width: parent.width
        height: 50
        color: "transparent"

        ColumnLayout
        {
            width: parent.width
            height: parent.height
            spacing: 1

            RowLayout
            {
                width: parent.width
                spacing: 10

                Item { width: 10 }

                Text
                {
                    text: "Interplanetary Transfer"
                    color: "#FFFFFF"
                    font.pointSize: 16
                    font.bold: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Button
                {
                    text: "Run"
                    icon.source: "/svg/play_arrow.svg"
                    font.pointSize: 10
                    font.bold: true
                    Material.background: "#4CAF50"
                    Material.foreground: "#FFFFFF"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    onClicked: __MissionInterplanetaryTransfer.simulate()

                    HoverHandler
                    {
                        acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                        cursorShape: Qt.PointingHandCursor
                    }
                }

                Item { width: 10 }
            }

            Rectangle
            {
                height: 3
                color: Material.color(Material.Grey)
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignBottom
            }
        }
    }

    footer: Rectangle
    {
        id: _footer_
        width: parent.width
        height: 50
        color: "transparent"

        ColumnLayout
        {
            anchors.fill: parent
            spacing: 10

            Rectangle
            {
                height: 3
                color: Material.color(Material.Grey)
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop
            }
        }
    }

    contentItem: Rectangle
    {
        width: parent.width
        color: "transparent"
    
        Figure
        {
            p_ObjectName: "InterplanetaryTransferFigure"
            r_Model: __InterplanetaryTransferFigure
            anchors.fill: parent
        }
    }
}