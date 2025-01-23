import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageOrbitInsertionLeft.js" as Script

import "../components/common"
import "../components/material"

// * The PageOrbitInsertionLeft class manages the orbit insertion left page.
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
                placeholderText: "Circular Parking Orbit Height [km]"
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

            RowLayout
            {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 20
                spacing: 10

                MaterialButton
                {
                    text: "Calculate Staging"
                    onClicked: __MissionOrbitInsertion.calculate_staging()
                }
            }
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
        }
    }
}