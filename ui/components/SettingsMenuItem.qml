import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle
{
    // * Menu item source icon.
    property string p_Icon: ""

    // * Menu item text.
    property string p_Text: ""

    // * Menu item mission type.
    property bool p_MissionType: false

    // * Menu item selected.
    property bool p_Selected: false

    // * Override to implement the "Click" action.
    function f_Click() {}

    // ! ----------------------------------------- ! //

    color: "transparent"
    width: 300
    height: _layout_.height + 20

    Rectangle
    {
        anchors.fill: parent
        radius: 5
        color: Material.color(p_MissionType ? Material.LightBlue : Material.LightGreen)
        opacity: 0.25
        visible: p_Selected
    }

    Rectangle
    {
        width: 3
        height: _layout_.height + 20
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        radius: 20
        color: Material.color(p_MissionType ? Material.LightBlue : Material.LightGreen)
        visible: p_Selected
    }
    
    MouseArea
    {
        id: _mouse_area_
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true
        onClicked: f_Click()
    }

    RowLayout
    {
        id: _layout_
        spacing: 20
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 10

        Rectangle
        {
            width: 54
            height: 54
            color: "#FFFFFF"
            radius: width / 2
            border.width: 3
            border.color: Material.color(p_MissionType ? Material.LightBlue : Material.LightGreen)

            Image
            {
                source: p_Icon
                sourceSize.width: 40
                sourceSize.height: 40
                anchors.centerIn: parent
            }
        }

        Text
        {
            text: p_Text
            color: Material.color(p_MissionType ? Material.LightBlue : Material.LightGreen)
            font.pointSize: 14
            font.bold: true
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle
    {
        anchors.fill: parent
        radius: 5
        color: Material.color(Material.Grey)
        opacity: 0.25
        visible: _mouse_area_.containsMouse
    }
}