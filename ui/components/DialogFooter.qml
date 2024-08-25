import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item
{
    // ? Override to implement the "Close" button action.
    function f_Close() {}

    // ? Override to implement the "Save" button action.
    function f_Save() {}

    // !-----------------------------------------! //

    id: root
    width: parent.width
    height: _layout_.height

    /*
    Rectangle
    {
        anchors.fill: parent
        opacity: 0.10
        color: Material.color(Material.Orange)
        bottomLeftRadius: 30
        bottomRightRadius: 30
    }
    */

    ColumnLayout
    {
        id: _layout_
        width: parent.width
        spacing: 0

        Rectangle
        {
            height: 3
            opacity: 0.25
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
        }

        RowLayout
        {
            spacing: 10
            Layout.fillWidth: true

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Save"
                font.pointSize: 10
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: "#4CAF50"
                onClicked: f_Save()
            }

            Button
            {
                text: "Close"
                font.pointSize: 10
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: "#F44336"
                onClicked: f_Close()
            }

            Item { width: 10 }
        }
    }
}