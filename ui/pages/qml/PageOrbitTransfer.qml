import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../js/PageOrbitTransfer.js" as Script

import "../../components/figure"
import "../../components/page"

// * The PageOrbitTransfer class manages the orbit transfer page.
Page
{
    // * Reference to the Maneuvers array.
    property var r_Maneuvers: []

    function update()
    {
        Script.loadManeuvers()
    }

    // ! ----------------------------------------- ! //

    background: Rectangle { color: "#424242" }
    header: PageHeader { p_Title: "Orbit Transfer" }
    footer: PageFooter {}

    contentItem: Item
    {
        width: parent.width

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