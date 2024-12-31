import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/dialog"
import "../components/material"

// * The DialogExit class manages the exit dialog.
Dialog
{
    // ! ----------------------------------------- ! //
    
    id: root
    title: "Quit"
    anchors.centerIn: parent
    modal: true
    font.pointSize: 12
    width: 350
    height: 200
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
        p_Title: "Quit"

        function f_Close()
        {
            close()
        }
    }

    footer: Item
    {
        width: parent.width
        height: 50

        RowLayout
        {
            width: parent.width
            height: 50
            spacing: 10

            Item
            {
                Layout.fillWidth: true
            }

            MaterialButton
            {
                text: "Yes"
                onClicked: Qt.quit()
            }

            MaterialButton
            {
                text: "No"
                onClicked: close()
            }

            Item
            {
                width: 10
            }
        }
    }

    contentItem: Item
    {
        ColumnLayout
        {
            spacing: 10
            Layout.alignment: Qt.AlignVCenter

            Label
            {
                text: "Do you want to close the application?"
            }
        }
    }
}