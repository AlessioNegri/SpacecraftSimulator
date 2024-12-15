import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtCharts

import "../components"

// ? The PageOrtbitInsertion class manages the orbit insertion page.
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
                    text: "Orbit Insertion"
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
                    onClicked: __MissionOrbitInsertion.simulate()

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
            p_ObjectName: "OrbitInsertionFigure"
            r_Model: __OrbitInsertionFigure
            anchors.fill: parent
        }

        /*
        ChartView
        {
            title: "Line Chart"
            titleColor: "#FFFFFF"
            anchors.fill: parent
            antialiasing: true
            //backgroundColor: "#424242"
            backgroundRoundness: 10
            
            LineSeries
            {
                name: "Line"
                XYPoint { x: 0; y: 0 }
                XYPoint { x: 1.1; y: 2.1 }
                XYPoint { x: 1.9; y: 3.3 }
                XYPoint { x: 2.1; y: 2.1 }
                XYPoint { x: 2.9; y: 4.9 }
                XYPoint { x: 3.4; y: 3.0 }
                XYPoint { x: 4.1; y: 3.3 }
            }
        }
        */
    }
}