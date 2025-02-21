import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../material"
import "../../dialogs"

// * The SideBar class manages the side bar component.
Rectangle
{
    // ! ----------------------------------------- ! //

    id: root
    anchors.top: parent.top
    anchors.left: parent.left
    anchors.bottom: parent.bottom
    width: 60
    color: "#162A35"
    radius: 10
    border.color: "#93F9D8"
    border.width: 2

    ColumnLayout
    {
        spacing: 10
        anchors.fill: parent
        anchors.margins: 10

        MaterialIcon
        {
            source: "/img/icon.svg"
            tooltip: "Home"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 0; loader.source = "pages/PageHome.qml" }
        }

        Rectangle
        {
            height: 2
            radius: 10
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
        }

        MaterialIcon
        {
            source: "/svg/launcher.svg"
            tooltip: "Launcher"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 1
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 1; loader.source = "pages/PageLauncher.qml" }
        }

        MaterialIcon
        {
            source: "/svg/spacecraft.svg"
            tooltip: "Spacecraft"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 2
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 2; loader.source = "pages/PageSpacecraft.qml" }
        }

        MaterialIcon
        {
            source: "/svg/capsule.svg"
            tooltip: "Capsule"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 3
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 3; loader.source = "pages/PageCapsule.qml" }
        }

        Rectangle
        {
            height: 2
            radius: 10
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
        }

        MaterialIcon
        {
            source: "/svg/orbit_insertion.svg"
            tooltip: "Orbit Insertion"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 4
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 4; loader.source = "pages/PageOrbitInsertion.qml" }
        }

        MaterialIcon
        {
            source: "/svg/orbit_transfer.svg"
            tooltip: "Orbit Transfer"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 5
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 5; loader.source = "pages/PageOrbitTransfer.qml" }
        }

        MaterialIcon
        {
            source: "/svg/orbit_propagation.svg"
            tooltip: "Orbit Propagation"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 6
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 6; loader.source = "pages/PageOrbitPropagation.qml" }
        }

        MaterialIcon
        {
            source: "/svg/interplanetary_transfer.svg"
            tooltip: "Interplanetary Transfer"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 7
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 7; loader.source = "pages/PageInterplanetaryTransfer.qml" }
        }

        MaterialIcon
        {
            source: "/svg/atmospheric_entry.svg"
            tooltip: "Atmospheric Entry"
            baseColor: "#93F9D8"
            hoverColor: "#FFEB3B"
            selectable: true
            checked: gp_CurrentPage === 8
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter

            function f_Click() { gp_CurrentPage = 8; loader.source = "pages/PageAtmosphericEntry.qml" }
        }

        Item
        {
            Layout.fillHeight: true
        }

        Rectangle
        {
            height: 2
            radius: 10
            color: Material.color(Material.Grey)
            Layout.fillWidth: true
        }

        MaterialIcon
        {
            source: "/svg/settings.svg"
            tooltip: "Settings"
            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
            
            function f_Click() { _dialog_settings_.open() }
        }

        MaterialIcon
        {
            source: "/svg/exit_to_app.svg"
            tooltip: "Exit"
            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
            
            function f_Click() { _dialog_exit_.open() }
        }

        MaterialIcon
        {
            source: "/svg/help.svg"
            tooltip: "About"
            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
            
            function f_Click() { _dialog_about_.open() }
        }
    }
}