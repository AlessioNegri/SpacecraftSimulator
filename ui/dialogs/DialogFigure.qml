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

    // ! ----------------------------------------- ! //

    id: root
    anchors.centerIn: parent
    modal: true
    width: window.width * 0.8
    height: window.height * 0.8
    closePolicy: Popup.NoAutoClose
    font.pointSize: 12
  
    header: DialogHeader
    {
        p_Title: root.title
    }

    footer: DialogFooter
    {
        p_ShowSaveButton: false

        function f_Close()
        {
            close()
        }
    }

    contentItem: Rectangle
    {
        color: "transparent"

        Figure
        {
            p_ObjectName: p_FigureCanvasName
            r_Model: p_FigureCanvasModel
            anchors.fill: parent
        }
    }
}