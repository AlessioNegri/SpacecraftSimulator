import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

import "DialogManeuvers.js" as Script

// ? The DialogManeuvers class manages the maneuvers dialog.
Dialog
{
    // ? Reference to the Maneuvers array.
    property var r_Maneuvers: []

    // ! ----------------------------------------- ! //

    id: root
    anchors.centerIn: parent
    modal: true
    width: window.width * 0.8
    height: window.height * 0.8
    closePolicy: Popup.NoAutoClose
    font.pointSize: 12

    onVisibleChanged: if (visible) Script.loadManeuvers()

    header: DialogHeader
    {
        p_Title: "Maneuvers"
    }

    footer: DialogFooter
    {
        function f_Close()
        {
            close()
        }

        function f_Save()
        {
            Script.saveManeuvers()
            
            close()
        }
    }

    contentItem: Rectangle
    {
        color: "transparent"

        ColumnLayout
        {
            width: parent.width
            height: parent.height
            spacing: 25
            
            Button
            {
                text: "Add Maneuver"
                icon.source: "/images/img/add.svg"
                font.pointSize: 12
                font.bold: true
                Material.background: "#009688"
                Material.foreground: "#FFFFFF"
                onClicked: Script.addManeuver()
            }

            Flickable
            {
                id: _scrollView_
                clip: true
                boundsBehavior: Flickable.StopAtBounds
                Layout.fillWidth: true
                Layout.fillHeight: true
                contentWidth: parent.width

                ScrollBar.vertical: ScrollBar { parent: _scrollView_; orientation: Qt.Vertical }

                ScrollBar.horizontal: ScrollBar { parent: _scrollView_; orientation: Qt.Horizontal }

                ColumnLayout
                {
                    id: _container_
                    spacing: 16
                    width: parent.width
                }
            }
        }
    }
}