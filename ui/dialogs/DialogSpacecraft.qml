import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

import "DialogSpacecraft.js" as Script

// ? The DialogSpacecraft class manages the spacecraft dialog.
Dialog
{
    // !-----------------------------------------! //

    id: root
    anchors.centerIn: parent
    modal: true
    width: window.width * 0.8
    height: window.height * 0.8
    closePolicy: Popup.NoAutoClose
    font.pointSize: 12

    onVisibleChanged: if (visible) Script.restoreParameters()

    header: DialogHeader
    {
        p_Title: "Spacecraft Properties"
    }

    footer: DialogFooter
    {
        function f_Close()
        {
            close()
        }

        function f_Save()
        {
            Script.saveParameters()
            
            close()
        }
    }

    contentItem: Rectangle
    {
        border.width: 2
        border.color: Material.color(Material.Orange)
        radius: 5
        color: "transparent"

        TabBar
        {
            id: _tab_bar_
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            background: Rectangle { color: "#33FF9800" }
            
            TabButton { text: "Propulsion"; font.bold: true }
            TabButton { text: "Aerodynamics"; font.bold: true }
            TabButton { text: "Atmospheric Entry"; font.bold: true }
        }

        StackLayout
        {
            width: parent.width
            currentIndex: _tab_bar_.currentIndex
            anchors.top: _tab_bar_.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 20

            // - Propulsion 

            Item
            {
                anchors.fill: parent

                GridLayout
                {
                    columns: 3
                    columnSpacing: 50
                    rowSpacing: 25
                    width: parent.width

                    DialogParameter
                    {
                        id: _initial_mass_
                        placeholderText: "Initial Mass [kg]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _specific_impulse_
                        placeholderText: "Specific Impulse [s]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _thrust_
                        placeholderText: "Thrust [N]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }
                }
            }

             // - Aerodynamics 

            Item
            {
                anchors.fill: parent

                GridLayout
                {
                    columns: 3
                    columnSpacing: 50
                    rowSpacing: 25
                    width: parent.width

                    DialogParameter
                    {
                        id: _lift_coefficient_
                        placeholderText: "Lift Coefficient"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _drag_coefficient_
                        placeholderText: "Drag Coefficient"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _reference_surface_
                        placeholderText: "Reference Surface [m^2]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }
                }
            }

            // - Atmospheric Entry 

            Item
            {
                anchors.fill: parent

                GridLayout
                {
                    columns: 3
                    columnSpacing: 50
                    rowSpacing: 25
                    width: parent.width

                    DialogParameter
                    {
                        id: _capsule_node_radius_
                        placeholderText: "Capsule Nose Radius [m]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _parachute_drag_coefficient_
                        placeholderText: "Parachute Drag Coeffient"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _parachute_reference_surface_
                        placeholderText: "Parachute Reference Surface [m^2]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _capsule_mass_
                        placeholderText: "Capsule Mass [kg]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _capsule_drag_coefficient_
                        placeholderText: "Capsule Drag Coefficient"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _capsule_lift_coefficient_
                        placeholderText: "Capsule Lift Coefficient"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }

                    DialogParameter
                    {
                        id: _capsule_reference_surface_
                        placeholderText: "Capsule Reference Surface [m^2]"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    }
                }
            }
        }
    }
}