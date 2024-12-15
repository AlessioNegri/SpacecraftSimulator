import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../js/SectionOrbitInsertion.js" as Script

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

    ColumnLayout
    {
        id: _layout_
        width: parent.width - 20
        spacing: 20

        // --- ENTRY CONDITIONS 

        SectionHeader
        {
            id: _pitchover_conditions_
            p_Title: "Pitchover Conditions"
            p_Icon: "/png/entry.png"
        }

        GridLayout
        {
            columns: 3
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
                placeholderText: "Final Integration Time [min]"
            }
        }
    }
}