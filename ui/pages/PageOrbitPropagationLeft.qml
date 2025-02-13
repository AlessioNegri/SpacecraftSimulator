import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageOrbitPropagationLeft.js" as Script

import "../components/common"
import "../components/material"

// * The PageOrbitPropagationLeft class manages the orbit propagation left page.
ScrollView
{
    // * Loads all the parameters.
    function load()
    {
        Script.restoreParameters()
    }

    // * Saves all the parameters.
    function save()
    {
        Script.saveParameters()

        load()
    }

    // ! ----------------------------------------- ! //

    Component.onCompleted: load()

    width: parent.width
    contentWidth: parent.width
    contentHeight: _layout_.height

    ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }
    ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }

    ColumnLayout
    {
        id: _layout_
        width: parent.width - 20
        spacing: 20

        // --- UNPERTURBED ORBIT 

        SectionHeader
        {
            id: _unperturbed_orbit_
            p_Title: "Unperturbed Orbit"
            p_Icon: "/png/orbit.png"
        }

        GridLayout
        {
            columns: 3
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_unperturbed_orbit_.p_Hide
            Layout.fillWidth: true

            SectionItemValue
            {
                id: _angular_momentum_
                placeholderText: "Angular Momentum [km^2/s]"
            }

            SectionItemValue
            {
                id: _eccentricity_
                placeholderText: "Eccentricity"
            }

            SectionItemValue
            {
                id: _inclination_
                placeholderText: "Inclination [deg]"
            }

            SectionItemValue
            {
                id: _raan_
                placeholderText: "RAAN [deg]"
            }

            SectionItemValue
            {
                id: _periapsis_anomaly_
                placeholderText: "Periapsis Anomaly [deg]"
            }

            SectionItemValue
            {
                id: _true_anomaly_
                placeholderText: "True Anomaly [deg]"
            }

            SectionItemValue
            {
                id: _start_date_
                placeholderText: "Start Date"
                inputMask: "0000-00-00 00:00:00;0"
                p_FloatRegex: false
            }

            SectionItemValue
            {
                id: _end_date_
                placeholderText: "End Date"
                inputMask: "0000-00-00 00:00:00;0"
                p_FloatRegex: false
            }
        }

        // --- PERTURBATIONS 

        SectionHeader
        {
            id: _perturbations_
            p_Title: "Perturbations"
            p_Icon: "/png/perturbations.png"
        }
        
        ColumnLayout
        {
            spacing: 20
            visible: !_perturbations_.p_Hide
            Layout.fillWidth: true

            CheckBox
            {
                id: _drag_
                text: "Drag"
                implicitHeight: 40
                Layout.fillWidth: true
            }

            CheckBox
            {
                id: _gravitational_
                text: "Gravitational"
                implicitHeight: 40
                Layout.fillWidth: true
            }

            CheckBox
            {
                id: _solar_radiation_pressure_
                text: "Solar Radiation Pressure"
                implicitHeight: 40
                Layout.fillWidth: true
            }

            RowLayout
            {
                spacing: 20
                Layout.fillWidth: true

                CheckBox
                {
                    id: _third_body_
                    text: "Third Body"
                    implicitHeight: 40
                    Layout.fillWidth: true
                }

                MaterialComboBox
                {
                    id: _third_body_combo_box_
                    implicitHeight: 40
                    model: [ "MOON", "SUN" ]
                    Layout.fillWidth: true
                }
            }
        }
    }
}