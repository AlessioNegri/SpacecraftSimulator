import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageAtmosphericEntryLeft.js" as Script

import "../dialogs/common"
import "../components/material"

// * The PageAtmosphericEntryLeft class manages the atmospheric entry left page.
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
            id: _entry_conditions_
            p_Title: "Entry Conditions"
            p_Icon: "/png/entry.png"
        }

        GridLayout
        {
            columns: 3
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_entry_conditions_.p_Hide
            Layout.fillWidth: true

            SectionItemValue
            {
                id: _entry_velocity_
                placeholderText: "Entry Velocity [km/s]"
            }

            SectionItemValue
            {
                id: _entry_flight_path_angle_
                placeholderText: "Entry Flight Path Angle [deg]"
            }

            SectionItemValue
            {
                id: _entry_altitude_
                placeholderText: "Entry Altitude [km]"
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

            Switch
            {
                id: _use_parachute_
                text: "Parachute"
                implicitHeight: 40
            }
        }
    }
}