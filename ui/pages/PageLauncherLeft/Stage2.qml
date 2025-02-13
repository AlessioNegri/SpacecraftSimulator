import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../components/common"
import "../../components/dialog"
import "../../components/material"

// * The Stage2 class manages the launcher left poge second stage.
ColumnLayout
{
    // * Loads all the parameters.
    function load()
    {
        // ? Mass

        _structural_mass_.text              = __MissionOrbitInsertion.stage_2.structural_mass
        _propellant_mass_.text              = __MissionOrbitInsertion.stage_2.propellant_mass
        _gross_mass_.text                   = __MissionOrbitInsertion.stage_2.gross_mass
        _payload_mass_.text                 = __MissionOrbitInsertion.stage_2.payload_mass
        _total_mass_.text                   = __MissionOrbitInsertion.stage_2.total_mass
        _propellant_fraction_.text          = __MissionOrbitInsertion.stage_2.propellant_fraction
        _structure_fraction_.text           = __MissionOrbitInsertion.stage_2.structure_fraction

        // ? Geometry

        _diameter_.text                     = __MissionOrbitInsertion.stage_2.diameter
        _height_.text                       = __MissionOrbitInsertion.stage_2.height
        _stage_cog_height_.text             = __MissionOrbitInsertion.stage_2.stage_center_of_gravity_height
        _stage_moi_.text                    = __MissionOrbitInsertion.stage_2.stage_moment_of_inertia
        _stack_cog_height_.text             = __MissionOrbitInsertion.stack_II_center_of_gravity_height
        _stack_moi_.text                    = __MissionOrbitInsertion.stack_II_moment_of_inertia

        // ? Propulsion

        _specific_impulse_.text             = __MissionOrbitInsertion.stage_2.vacuum_specific_impulse
        _thrust_.text                       = __MissionOrbitInsertion.stage_2.vacuum_thrust
        _propellant_mass_flow_rate_.text    = __MissionOrbitInsertion.stage_2.propellant_mass_flow_rate
        _burn_time_.text                    = __MissionOrbitInsertion.stage_2.burn_time
        _thrust_to_weight_ratio_.text       = __MissionOrbitInsertion.stage_2.thrust_to_weight_ratio

        // ? Aerodynamics

        _drag_coefficient_.text             = __MissionOrbitInsertion.stage_2.drag_coefficient
        _lift_coefficient_.text             = __MissionOrbitInsertion.stage_2.lift_coefficient
        _reference_surface_.text            = __MissionOrbitInsertion.stage_2.reference_surface
    }

    // * Saves all the parameters.
    function save()
    {
        // ? Mass

        __MissionOrbitInsertion.stage_2.structural_mass         = _structural_mass_.text 
        __MissionOrbitInsertion.stage_2.propellant_mass         = _propellant_mass_.text
        
        // ? Geometry

        __MissionOrbitInsertion.stage_2.diameter                = _diameter_.text
        __MissionOrbitInsertion.stage_2.height                  = _height_.text

        // ? Propulsion

        __MissionOrbitInsertion.stage_2.vacuum_specific_impulse = _specific_impulse_.text
        __MissionOrbitInsertion.stage_2.vacuum_thrust           = _thrust_.text
        
        // ? Aerodynamics

        __MissionOrbitInsertion.stage_2.drag_coefficient        = _drag_coefficient_.text
        __MissionOrbitInsertion.stage_2.lift_coefficient        = _lift_coefficient_.text

        load()
    }

    // ! ----------------------------------------- ! //

    id: _layout_
    width: parent.width - 20
    spacing: 20

    // --- MASS 

    SectionHeader
    {
        id: _mass_
        p_Title: "Mass"
        p_Icon: "/png/mass.png"
    }

    GridLayout
    {
        columns: 2
        rowSpacing: 20
        columnSpacing: 20
        visible: !_mass_.p_Hide
        Layout.fillWidth: true

        SectionItemName
        {
            text: "Structural Mass [kg]"
        }

        SectionItemValue
        {
            id: _structural_mass_
        }

        SectionItemName
        {
            text: "Propellant Mass [kg]"
        }

        SectionItemValue
        {
            id: _propellant_mass_
        }

        GridLayout
        {
            columns: 3
            rowSpacing: 10
            columnSpacing: 10
            Layout.columnSpan: 2
            Layout.fillWidth: true
            
            SectionItemValue
            {
                id: _gross_mass_
                placeholderText: "Gross Mass [kg]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _payload_mass_
                placeholderText: "Payload Mass [kg]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _total_mass_
                placeholderText: "Total Mass [kg]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _propellant_fraction_
                placeholderText: "Propellant Fraction []"
                readOnly: true
            }

            SectionItemValue
            {
                id: _structure_fraction_
                placeholderText: "Structure Fraction []"
                readOnly: true
            }
        }
    }

    // --- GEOMETRY 

    SectionHeader
    {
        id: _geometry_
        p_Title: "Geometry"
        p_Icon: "/png/structure.png"
    }

    GridLayout
    {
        columns: 2
        rowSpacing: 20
        columnSpacing: 20
        visible: !_geometry_.p_Hide
        Layout.fillWidth: true

        SectionItemName
        {
            text: "Diameter [m]"
        }

        SectionItemValue
        {
            id: _diameter_
        }

        SectionItemName
        {
            text: "Height [m]"
        }

        SectionItemValue
        {
            id: _height_
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 10
            columnSpacing: 10
            Layout.columnSpan: 2
            Layout.fillWidth: true
            
            SectionItemValue
            {
                id: _stage_cog_height_
                placeholderText: "Stage Center Of Gravity Height [m]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _stage_moi_
                placeholderText: "Stage Moment Of Inertia [kg * m^2]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _stack_cog_height_
                placeholderText: "Stack Center Of Gravity Height [m]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _stack_moi_
                placeholderText: "Stack Moment Of Inertia [kg * m^2]"
                readOnly: true
            }
        }
    }

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
            text: "Vacuum Specific Impulse [s]"
        }

        SectionItemValue
        {
            id: _specific_impulse_
        }

        SectionItemName
        {
            text: "Vacuum Thrust [N]"
        }

        SectionItemValue
        {
            id: _thrust_
        }

        RowLayout
        {
            spacing: 10
            Layout.columnSpan: 2
            Layout.fillWidth: true
            
            SectionItemValue
            {
                id: _propellant_mass_flow_rate_
                placeholderText: "Propellant Mass Flow Rate [kg/s]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _burn_time_
                placeholderText: "Burn Time [s]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _thrust_to_weight_ratio_
                placeholderText: "Thrust / Weight []"
                readOnly: true
            }
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
            text: "Drag Coefficient [-]"
        }

        SectionItemValue
        {
            id: _drag_coefficient_
        }

        SectionItemName
        {
            text: "Lift Coefficient [-]"
        }

        SectionItemValue
        {
            id: _lift_coefficient_
        }

        RowLayout
        {
            spacing: 10
            Layout.columnSpan: 2
            Layout.fillWidth: true
            
            SectionItemValue
            {
                id: _reference_surface_
                placeholderText: "Reference Surface [m^2]"
                readOnly: true
            }
        }
    }
}