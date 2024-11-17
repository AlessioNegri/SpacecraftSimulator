import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

import "js/PageOrbitTransfer.js" as Script

// ? The PageOrbitTransfer class manages the orbit transfer page.
Page
{
    // * Reference to the Maneuvers array.
    property var r_Maneuvers: []

    // ! ----------------------------------------- ! //

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
                    text: "Orbit Transfer"
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
                    onClicked: {

                        __MissionOrbitTransfer.simulate()

                        Script.loadManeuvers()
                    }

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

        Rectangle
        {
            id: _box_
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.margins: 10
            width: parent.width * 0.25
            color: "transparent"
            border.color: Material.color(Material.Orange)
            border.width: 3
            radius: 10

            ScrollView
            {
                anchors.fill: parent
                padding: 20
                //contentWidth: _container_.width
                contentHeight: _container_.height

                ColumnLayout
                {
                    id: _container_
                    spacing: 20
                    width: parent.width
                }
            }
        }

        Figure
        {
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.left: _box_.right
            p_ObjectName: "OrbitTransferFigure"
            r_Model: __OrbitTransferFigure
        }
    }
}