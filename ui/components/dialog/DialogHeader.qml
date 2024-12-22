import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

import "../material"

// * The DialogHeader class manages the dialog header.
Item
{
    // * Title.
    property string p_Title: ""

    // * True for showing the save button.
    property bool p_ShowSaveButton: false

    // * True for showing the update button.
    property bool p_ShowUpdateButton: false

    // * Override to implement the "Save" button action.
    function f_Save() {}

    // * Override to implement the "Update" button action.
    function f_Update() {}

    // * Override to implement the "Close" button action.
    function f_Close() {}

    // ! ----------------------------------------- ! //

    id: root
    width: parent.width
    height: _layout_.height
    
    ColumnLayout
    {
        id: _layout_
        width: parent.width
        height: 70
        spacing: 0
        
        RowLayout
        {
            spacing: 10

            Item
            {
                width: 10
            }

            Text
            {
                text: p_Title
                font.pointSize: 24
                font.bold: true
                color: Material.color(Material.Orange)
            }

            Item
            {
                Layout.fillWidth: true
            }

            MaterialIcon
            {
                source: "/svg/save.svg"
                visible: p_ShowSaveButton

                function f_Click() { f_Save() }
            }

            MaterialIcon
            {
                source: "/svg/update.svg"
                visible: p_ShowUpdateButton

                function f_Click() { f_Update() }
            }

            MaterialIcon
            {
                source: "/svg/clear.svg"

                function f_Click() { f_Close() }
            }

            Item
            {
                width: 10
            }
        }

        Rectangle
        {
            height: 3
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
        }
    }
}