import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

// ? The PageAtmosphericEntry class manages the orbital perturbations page.
Page
{
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
                    text: "Atmospheric Entry"
                    color: "#FFFFFF"
                    font.pointSize: 16
                    font.bold: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Button
                {
                    font.pointSize: 10
                    font.bold: true
                    icon.source: "/images/img/play_arrow.svg"
                    Material.background: Material.Red
                    Material.foreground: "#FFFFFF"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    onClicked: __MissionAtmosphericEntry.simulate()
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
            p_ObjectName: "AtmosphericEntryFigure"
            r_Model: __AtmosphericEntryFigure
            anchors.fill: parent
        }
    }
}