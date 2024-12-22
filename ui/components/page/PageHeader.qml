import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// * The PageHeader class manages the page header.
Item
{
    // * Title.
    property string p_Title: ""

    // ! ----------------------------------------- ! //

    id: root
    width: parent.width
    height: 50

    ColumnLayout
    {
        anchors.fill: parent
        spacing: 1

        Text
        {
            text: p_Title
            color: "#FFFFFF"
            font.pointSize: 20
            font.bold: true
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
        }

        Rectangle
        {
            height: 3
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignBottom
        }
    }
}