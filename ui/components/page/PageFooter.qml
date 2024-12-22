import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// * The PageFooter class manages the page footer.
Item
{
    // ! ----------------------------------------- ! //

    id: root
    width: parent.width
    height: 50

    ColumnLayout
    {
        anchors.fill: parent
        spacing: 1

        Rectangle
        {
            height: 3
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
        }
    }
}