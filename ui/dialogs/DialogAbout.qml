import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/dialog"

// * The DialogAbout class manages the about dialog.
Dialog
{
    // ! ----------------------------------------- ! //
    
    id: root
    title: "About - Spacecraft Simulator"
    anchors.centerIn: parent
    modal: true
    font.pointSize: 12
    width: 625
    height: 275
    closePolicy: Popup.NoAutoClose

    background: Rectangle
    {
        color: "#162A35"
        radius: 10
        border.width: 2
        border.color: "#93F9D8"
    }

    Shortcut
    {
        sequence: StandardKey.Escape
        context: Qt.ApplicationShortcut
        onActivated: close()
    }

    header: DialogHeader
    {
        p_Title: "About - Spacecraft Simulator"

        function f_Close()
        {
            close()
        }
    }

    contentItem: Item
    {
        RowLayout
        {
            spacing: 100

            Rectangle
            {
                width: 150
                height: 150
                color: "transparent"

                Image
                {
                    source: "/img/icon.png"
                    fillMode: Image.PreserveAspectFit
                    anchors.fill: parent
                }
            }

            ColumnLayout
            {
                spacing: 10
                Layout.alignment: Qt.AlignVCenter

                Label
                {
                    text: "Spacecraft Simulator 1.0.0"
                    font.bold: true
                }

                Label
                {
                    text: "Released on Jan 01 2025"
                }

                Label
                {
                    text: "Copyright 2025 Alessio Negri. All rights reserved."
                }
            }
        }
    }
}