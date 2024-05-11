import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// ? The DialogAbout class manages the about dialog.
Dialog
{
    title: "About - Spacecraft Simulator"
    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 700
    height: 400

    header: Item
    {
        width: parent.width
        height: 75

        Text
        {
            text: title
            padding: 20
            font.pointSize: 24
            font.bold: true
            color: Material.color(Material.Indigo)
        }
    }

    footer: Item
    {
        width: parent.width
        height: 60
        
        RowLayout
        {
            width: parent.width

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Ok"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: close()
            }

            Item { width: 10 }
        }
    }

    Item
    {
        Row
        {
            padding: 10
            spacing: 100

            Image
            {
                source: "/images/img/icon.png"
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