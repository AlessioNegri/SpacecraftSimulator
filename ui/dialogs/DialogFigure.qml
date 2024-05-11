import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

// ? The DialogFigure class manages the generic figure dialog.
Dialog
{
    // ? Name of the backend figure canvas.
    property string p_FigureCanvasName: ""

    // ? Reference of the backend figure canvas.
    property var p_FigureCanvasModel: null

    //!-----------------------------------------!//

    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 1200
    height: 800
  
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

    Figure {
        p_ObjectName: p_FigureCanvasName
        r_Model: p_FigureCanvasModel
        anchors.fill: parent
    }
}