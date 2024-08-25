import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item
{
    // ? Title.
    property string p_Title: ""

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
        topLeftRadius: 30
        topRightRadius: 30
    }
    */
    
    ColumnLayout
    {
        id: _layout_
        width: parent.width
        spacing: 10
        
        Text
        {
            text: p_Title
            leftPadding: 20
            topPadding: 10
            font.pointSize: 20
            font.bold: true
            color: Material.color(Material.Orange)
        }

        Rectangle
        {
            height: 3
            opacity: 0.25
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
        }
    }
}