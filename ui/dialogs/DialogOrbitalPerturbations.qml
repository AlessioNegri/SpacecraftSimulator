import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

import "DialogOrbitalPerturbations.js" as Script

// ? The DialogOrbitalPerturbations class manages the orbit perturbations dialog.
Dialog
{
    // ! ----------------------------------------- ! //

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
        p_Title: "Orbital Perturbations"
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

            // --- INITIAL CONDITIONS 

            Text
            {
                text: "Initial Conditions"
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
                    id: _angular_momentum_
                    placeholderText: "Angular Momentum [km^2/s]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _eccentricity_
                    placeholderText: "Eccentricity"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _inclination_
                    placeholderText: "Inclination [deg]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _raan_
                    placeholderText: "RAAN [deg]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _periapsis_anomaly_
                    placeholderText: "Periapsis Anomaly [deg]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _true_anomaly_
                    placeholderText: "True Anomaly [deg]"
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

            // --- PERTURBATIONS 

            Text
            {
                text: "Perturbations"
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
                    id: _start_date_
                    placeholderText: "Start Date"
                    inputMask: "0000-00-00 00:00:00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _end_date_
                    placeholderText: "End Date"
                    inputMask: "0000-00-00 00:00:00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }
                
                CheckBox
                {
                    id: _drag_
                    text: "Drag"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                CheckBox
                {
                    id: _gravitational_
                    text: "Gravitational"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                CheckBox
                {
                    id: _solar_radiation_pressure_
                    text: "Solar Radiation Pressure"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                CheckBox
                {
                    id: _third_body_
                    text: "Third Body"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                ComboBox
                {
                    id: _third_body_combo_box_
                    implicitHeight: 50
                    model: [ "MOON", "SUN" ]
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }
            }
        }
    }
}
