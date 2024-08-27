import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

import "DialogAtmosphericEntryConditions.js" as Script

// ? The DialogAtmosphericEntryConditions class manages the atmospheric entry conditions dialog.
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
        p_Title: "Entry Conditions"
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
        color: "transparent"

        ColumnLayout
        {
            width: parent.width
            spacing: 25

            // - PARAMETERS 

            Text
            {
                text: "Parameters"
                color: "#FFFFFF"
                font.pointSize: 16
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            }

            RowLayout
            {
                spacing: 50
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                
                DialogParameter
                {
                    id: _entry_velocity_
                    placeholderText: "Entry Velocity [km/s]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _entry_flight_path_angle_
                    placeholderText: "Entry Flight Path Angle [deg]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _entry_altitude_
                    placeholderText: "Entry Altitude [km]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _final_integration_time_
                    placeholderText: "Final Integration Time [min]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                Switch
                {
                    id: _use_parachute_
                    text: "Use Parachute"
                    font.pointSize: 12
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }
            }

            Rectangle
            {
                height: 3
                radius: 3
                color: Material.color(Material.Orange)
                Layout.fillWidth: true
            }

            // - RESULTS 

            Text
            {
                text: "Results"
                color: "#FFFFFF"
                font.pointSize: 16
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            }

            RowLayout
            {
                spacing: 50
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                
                DialogParameter
                {
                    id: _impact_velocity_
                    text: __MissionAtmosphericEntry.impact_velocity
                    placeholderText: "Impact Velocity [m/s]"
                    readOnly: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }
            }
        }
    }
}