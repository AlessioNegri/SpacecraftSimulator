import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// * The PageFooter class manages the page footer.
Item
{
    // ! ----------------------------------------- ! //

    id: root
    width: parent.width
    height: 25

    ColumnLayout
    {
        anchors.fill: parent
        spacing: 1

        Rectangle
        {
            height: 1
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
        }

        RowLayout
        {
            spacing: 10
            Layout.fillWidth: true
            
            Text
            {
                text: "© 2025 Alessio Negri"
                font.pointSize: 10
                color: "#FFFFFF"
            }

            Item
            {
                Layout.fillWidth: true
            }

            Text
            {
                text: "Version 1.0.0"
                font.pointSize: 10
                color: "#FFFFFF"
            }

            Item {}
        }
    }
}