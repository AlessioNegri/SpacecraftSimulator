import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../js/SectionOrbitInsertion.js" as Script

import "../../common"
import "../../../components/material"

// * The SectionOrbitInsertion class manages the orbit insertion section.
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

    width: parent.width
    contentWidth: parent.width
    contentHeight: _layout_.height
    onVisibleChanged: if (visible) load()

    ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }

    ColumnLayout
    {
        id: _layout_
        width: parent.width - 20
        spacing: 20

        // --- ENTRY CONDITIONS 

        SectionHeader
        {
            id: _pitchover_conditions_
            p_Title: "Design Conditions"
            p_Icon: "/png/entry.png"
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_pitchover_conditions_.p_Hide
            Layout.fillWidth: true

            SectionItemValue
            {
                id: _pitchover_height_
                placeholderText: "Pitchover Height [m]"
            }

            SectionItemValue
            {
                id: _pitchover_flight_path_angle_
                placeholderText: "Pitchover Flight Path Angle [deg]"
            }

            SectionItemValue
            {
                id: _circular_parking_orbit_height_
                placeholderText: "Circular Parking Orbit Height [m]"
            }

            SectionItemValue
            {
                id: _circular_parking_orbit_velocity_
                placeholderText: "Circular Parking Orbit Velocity [km/s]"
                readOnly: true
            }
        }

        // --- PARAMETERS 

        SectionHeader
        {
            id: _parameters_
            p_Title: "Parameters"
            p_Icon: "/png/parameters.png"
        }
        
        ColumnLayout
        {
            spacing: 20
            visible: !_parameters_.p_Hide
            Layout.fillWidth: true

            SectionItemValue
            {
                id: _final_integration_time_
                placeholderText: "Final Integration Time [s]"
            }

            RowLayout
            {
                spacing: 10
                Layout.fillWidth: true

                Switch
                {
                    id: _use_stage_1_
                    text: "Stage 1"
                    implicitHeight: 40
                }

                SectionItemValue
                {
                    id: _thrust_to_weight_ratio_1_
                    placeholderText: "Thrust / Weight []"
                }

                SectionItemValue
                {
                    id: _average_flight_path_angle_1_
                    placeholderText: "Average FPA [deg]"
                }

                SectionItemValue
                {
                    id: _structure_ratio_1_
                    placeholderText: "Structure Ratio []"
                }
            }

            RowLayout
            {
                spacing: 10
                Layout.fillWidth: true

                Switch
                {
                    id: _use_stage_2_
                    text: "Stage 2"
                    implicitHeight: 40
                }

                SectionItemValue
                {
                    id: _thrust_to_weight_ratio_2_
                    placeholderText: "Thrust / Weight []"
                }

                SectionItemValue
                {
                    id: _average_flight_path_angle_2_
                    placeholderText: "Average FPA [deg]"
                }

                SectionItemValue
                {
                    id: _structure_ratio_2_
                    placeholderText: "Structure Ratio []"
                }

                SectionItemValue
                {
                    id: _burnout_time_1_
                    placeholderText: "Burnout Time - Stage 1 [s]"
                }
            }

            RowLayout
            {
                spacing: 10
                Layout.fillWidth: true

                Switch
                {
                    id: _use_stage_3_
                    text: "Stage 3"
                    implicitHeight: 40
                }

                SectionItemValue
                {
                    id: _thrust_to_weight_ratio_3_
                    placeholderText: "Thrust / Weight []"
                }

                SectionItemValue
                {
                    id: _average_flight_path_angle_3_
                    placeholderText: "Average FPA [deg]"
                }

                SectionItemValue
                {
                    id: _structure_ratio_3_
                    placeholderText: "Structure Ratio []"
                }

                SectionItemValue
                {
                    id: _burnout_time_2_
                    placeholderText: "Burnout Time - Stage 2 [s]"
                }
            }

            Button
            {
                text: "Calculate Staging"
                font.bold: true
                Material.background: "#FF5722"
                onClicked: __MissionOrbitInsertion.calculate_staging()
            }
        }
    }
}