import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/material"
import "../components/page"

// * The PageCapsule class manages the capsule page.
Page
{
    // ! ----------------------------------------- ! //

    //background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Capsule"; p_Source: "/png/capsule.png" }
    footer: PageFooter {}

    contentItem: Item
    {
        RowLayout
        {
            spacing: 10
            anchors.fill: parent
            anchors.margins: 10

            PageBox
            {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout
                {
                    anchors.fill: parent
                    anchors.margins: 10

                    RowLayout
                    {
                        Layout.fillWidth: true
                        spacing: 10

                        Text
                        {
                            text: "Parameters"
                            font.pointSize: 20
                            font.bold: true
                            color: "#93F9D8"
                        }

                        Item
                        {
                            Layout.fillWidth: true
                        }

                        MaterialIcon
                        {
                            source: "/svg/save.svg"

                            function f_Click()
                            {
                                _section_.save()

                                notification_text.text = "Parameters Saved"
                                
                                notification.start()
                            }
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        radius: 10
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignBottom
                    }

                    PageCapsuleLeft
                    {
                        id: _section_
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }
        }
    }
}