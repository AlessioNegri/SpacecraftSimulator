import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item
{
    // ? True for showing the save button.
    property bool p_ShowSaveButton: true

    // ? True for showing the update button.
    property bool p_ShowUpdateButton: false

    // ? Override to implement the "Close" button action.
    function f_Close() {}

    // ? Override to implement the "Save" button action.
    function f_Save() {}

    // ? Override to implement the "Update" button action.
    function f_Update() {}

    // ! ----------------------------------------- ! //

    id: root
    width: parent.width
    height: _layout_.height

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
                text: "Update"
                visible: p_ShowUpdateButton
                font.pointSize: 10
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: "#3F51B5"
                onClicked: f_Update()
            }

            Button
            {
                text: "Save"
                visible: p_ShowSaveButton
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