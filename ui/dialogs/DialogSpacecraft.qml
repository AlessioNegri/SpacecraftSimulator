import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "DialogSpacecraft.js" as Script

// ? The DialogSpacecraft class manages the spacecraft dialog.
Dialog
{
    //!-----------------------------------------!//

    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 1100
    height: 700

    header: Item
    {
        width: parent.width
        height: 75

        Text
        {
            text: "Spacecraft Properties"
            padding: 20
            font.pointSize: 24
            font.bold: true
            color: Material.color(Material.Indigo)
        }
    }

    footer: Item
    {
        width: parent.width
        height: 70
        
        RowLayout
        {
            width: parent.width

            Item { width: 10 }

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Save"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: { Script.saveParameters(); close() }
            }

            Button
            {
                text: "Close"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Grey
                Material.foreground: "#FFFFFF"
                onClicked: close()
            }

            Item { width: 10 }
        }
    }

    GridLayout
    {
        columns: 3
        columnSpacing: 20
        rowSpacing: 20

        Label { text: "Initial Mass"; Layout.alignment: Qt.AlignHCenter }
        
        TextField
        {
            id: _m_0_
            text: __Spacecraft.initial_mass
            validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
            implicitWidth: 200
        }

        Label { text: "[kg]" }
        
        Label { text: "Specific Impulse"; Layout.alignment: Qt.AlignHCenter }

        TextField
        {
            id: _I_sp_
            text: __Spacecraft.specific_impulse
            validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
            Layout.fillWidth: true
        }

        Label { text: "[s]" }

        Label { text: "Thrust"; Layout.alignment: Qt.AlignHCenter }

        TextField
        {
            id: _T_
            text: __Spacecraft.thrust
            validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
            Layout.fillWidth: true
        }

        Label { text: "[N]" }
    }
}