import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

// ? The DialogAbout class manages the about dialog.
Dialog
{
    // ! ----------------------------------------- ! //
    
    id: root
    title: "About - Spacecraft Simulator"
    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 700
    height: 400

    header: DialogHeader
    {
        p_Title: "About - Spacecraft Simulator"
    }

    footer: DialogFooter
    {
        p_ShowSaveButton: false
        
        function f_Close()
        {
            close()
        }
    }

    contentItem: Item
    {
        Row
        {
            padding: 10
            spacing: 100

            Image
            {
                source: "/img/icon.png"
                fillMode: Image.PreserveAspectFit
                width: 200
                height: width
            }

            ColumnLayout
            {
                spacing: 10

                Label
                {
                    text: "Spacecraft Simulator 1.0"
                    font.pointSize: 16
                    font.bold: true
                }

                Label
                {
                    text: "Released on Jan 01 2025"
                    font.pointSize: 12
                }

                Label
                {
                    text: "Copyright 2025 Alessio Negri. All rights reserved."
                    font.pointSize: 12
                }
            }
        }
    }
}