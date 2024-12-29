import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/dialog"
import "../components/figure"

// * The DialogFigure class manages the generic figure dialog.
Dialog
{
    // * Name of the backend figure canvas.
    property string p_FigureCanvasName: ""

    // * Reference of the backend figure canvas.
    property var p_FigureCanvasModel: null

    // ! ----------------------------------------- ! //

    id: root
    anchors.centerIn: parent
    modal: true
    width: parent.width * 0.95
    height: parent.height * 0.95
    font.pointSize: 12

    Shortcut
    {
        sequence: StandardKey.Cancel
        context: Qt.ApplicationShortcut
        onActivated: close()
    }
  
    header: DialogHeader
    {
        p_Title: root.title

        function f_Close()
        {
            close()
        }
    }

    contentItem: Item
    {
        Figure
        {
            p_ObjectName: p_FigureCanvasName
            r_Model: p_FigureCanvasModel
            anchors.fill: parent
        }
    }
}