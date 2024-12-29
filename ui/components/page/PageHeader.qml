import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../material"

// * The PageHeader class manages the page header.
Item
{
    // * Title.
    property string p_Title: ""

    // * Icon source file.
    property string p_Source: ""

    // ! ----------------------------------------- ! //

    id: root
    width: parent.width
    height: 50

    RowLayout
    {
        anchors.fill: parent
        spacing: 10

        Item {}

        Image
        {
            source: p_Source
            sourceSize.width: 32
            sourceSize.height: 32
            fillMode: Image.PreserveAspectFit
        }

        Text
        {
            text: p_Title
            color: "#93F9D8"
            font.pointSize: 20
            font.bold: true
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignLeft
        }

        Item
        {
            Layout.fillWidth: true
        }
    }
}