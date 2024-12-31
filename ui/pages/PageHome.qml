import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/page"

// * The PageHome class manages the home page.
Page
{
    // ! ----------------------------------------- ! //

    //background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Spacecraft Simulator" }
    footer: PageFooter {}

    contentItem: Item
    {
        GridLayout
        {
            rows: 2
            columns: 2
            rowSpacing: 50
            columnSpacing: 50
            uniformCellWidths: true
            anchors.fill: parent
            anchors.margins: 50
            clip: true

            Text
            {
                text: "Configure The Systems..."
                color: "#FFFFFF"
                font.pointSize: 24
                font.bold: true
                height: 100
                Layout.alignment: Qt.AlignHCenter
            }

            Text
            {
                text: "...Explore The Missions"
                color: "#FFFFFF"
                font.pointSize: 24
                font.bold: true
                height: 100
                Layout.alignment: Qt.AlignHCenter
            }

            ColumnLayout
            {
                spacing: 10
                Layout.fillWidth: true
                Layout.fillHeight: true

                InfoBox
                {
                    p_Image: "/jpg/launcher.jpg"
                    p_Icon: "/png/launcher.png"
                    p_Text: "Launcher"
                    p_PageIndex: 1
                    p_PageLink: "pages/PageLauncher.qml"
                }

                InfoBox
                {
                    p_Image: "/jpg/spacecraft.jpg"
                    p_Icon: "/png/spacecraft.png"
                    p_Text: "Spacecraft"
                    p_PageIndex: 2
                    p_PageLink: "pages/PageSpacecraft.qml"
                }

                InfoBox
                {
                    p_Image: "/jpg/capsule.jpg"
                    p_Icon: "/png/capsule.png"
                    p_Text: "Capsule"
                    p_PageIndex: 3
                    p_PageLink: "pages/PageCapsule.qml"
                }
            }

            ColumnLayout
            {
                spacing: 10
                Layout.fillWidth: true
                Layout.fillHeight: true

                InfoBox
                {
                    p_Image: "/jpg/orbit_insertion.jpg"
                    p_Icon: "/png/orbit_insertion.png"
                    p_Text: "Orbit Insertion"
                    p_PageIndex: 4
                    p_PageLink: "pages/PageOrbitInsertion.qml"
                }

                InfoBox
                {
                    p_Image: "/jpg/orbit_transfer.jpg"
                    p_Icon: "/png/orbit_transfer.png"
                    p_Text: "Orbit Transfer"
                    p_PageIndex: 5
                    p_PageLink: "pages/PageOrbitTransfer.qml"
                }

                InfoBox
                {
                    p_Image: "/jpg/orbit_propagation.jpg"
                    p_Icon: "/png/orbit_propagation.png"
                    p_Text: "Orbit Propagation"
                    p_PageIndex: 6
                    p_PageLink: "pages/PageOrbitPropagation.qml"
                }

                InfoBox
                {
                    p_Image: "/jpg/interplanetary_transfer.jpg"
                    p_Icon: "/png/interplanetary_transfer.png"
                    p_Text: "Interplanetary Transfer"
                    p_PageIndex: 7
                    p_PageLink: "pages/PageInterplanetaryTransfer.qml"
                }

                InfoBox
                {
                    p_Image: "/jpg/atmospheric_entry.jpg"
                    p_Icon: "/png/atmospheric_entry.png"
                    p_Text: "Atmospheric Entry"
                    p_PageIndex: 8
                    p_PageLink: "pages/PageAtmosphericEntry.qml"
                }
            }
        }
    }
}