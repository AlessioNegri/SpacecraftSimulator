import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageSpacecraftLeft.js" as Script

import "../dialogs/common"
import "../components/material"

// * The PageSpacecraftLeft class manages the spacecraft left page.
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

        // --- PROPULSION 

        SectionHeader
        {
            id: _propulsion_
            p_Title: "Propulsion"
            p_Icon: "/png/propulsion.png"
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 20
            columnSpacing: 20
            visible: !_propulsion_.p_Hide
            Layout.fillWidth: true

            SectionItemName
            {
                text: "Initial Mass [kg]"
            }

            SectionItemValue
            {
                id: _initial_mass_
            }

            SectionItemName
            {
                text: "Specific Impulse [s]"
            }

            SectionItemValue
            {
                id: _specific_impulse_
            }

            SectionItemName
            {
                text: "Thrust [N]"
            }

            SectionItemValue
            {
                id: _thrust_
            }
        }

        // --- AERODYNAMICS 

        SectionHeader
        {
            id: _aerodynamics_
            p_Title: "Aerodynamics"
            p_Icon: "/png/aerodynamics.png"
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 20
            columnSpacing: 20
            visible: !_aerodynamics_.p_Hide
            Layout.fillWidth: true

            SectionItemName
            {
                text: "Lift Coefficient [-]"
            }

            SectionItemValue
            {
                id: _lift_coefficient_
            }

            SectionItemName
            {
                text: "Drag Coefficient [-]"
            }

            SectionItemValue
            {
                id: _drag_coefficient_
            }

            SectionItemName
            {
                text: "Reference Surface [m^2]"
            }

            SectionItemValue
            {
                id: _reference_surface_
            }
        }

        // --- SOLAR RADIATION PRESSURE 

        SectionHeader
        {
            id: _solar_radiation_pressure_
            p_Title: "Solar Radiation Pressure"
            p_Icon: "/png/solar_radiation_pressure.png"
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 20
            columnSpacing: 20
            visible: !_solar_radiation_pressure_.p_Hide
            Layout.fillWidth: true

            SectionItemName
            {
                text: "Radiation Pressure Coefficient [-]"
            }

            SectionItemValue
            {
                id: _radiation_pressure_coefficient_
            }

            SectionItemName
            {
                text: "Absorbing Surface [m^2]"
            }

            SectionItemValue
            {
                id: _absorbing_surface_
            }
        }
    }
}