import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageLauncherLeft.js" as Script

import "../dialogs/common"
import "../components/dialog"
import "../components/material"

// * The PageLauncherLeft class manages the launcher left poge.
ScrollView
{
    // * Selected stage.
    property int p_CurrentStage: 1

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

    width: parent.width - 20
    contentWidth: parent.width
    contentHeight: _layout_.height

    ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }
    ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }

    ColumnLayout
    {
        id: _layout_
        width: parent.width - 20
        spacing: 20

        // --- STRUCTURE 

        SectionHeader
        {
            id: _structural_
            p_Title: "Structure"
            p_Icon: "/png/structure.png"
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 20
            columnSpacing: 20
            visible: !_structural_.p_Hide
            Layout.fillWidth: true

            // >>> Stage 1

            SectionItemName
            {
                text: "Structural Mass [kg]"
                visible: p_CurrentStage === 1
            }

            SectionItemValue
            {
                id: _structural_mass_1_
                visible: p_CurrentStage === 1
            }

            SectionItemName
            {
                text: "Propellant Mass [kg]"
                visible: p_CurrentStage === 1
            }

            SectionItemValue
            {
                id: _propellant_mass_1_
                visible: p_CurrentStage === 1
            }

            SectionItemName
            {
                text: "Diameter [m]"
                visible: p_CurrentStage === 1
            }

            SectionItemValue
            {
                id: _diameter_1_
                visible: p_CurrentStage === 1
            }

            GridLayout
            {
                columns: 3
                rowSpacing: 10
                columnSpacing: 10
                visible: p_CurrentStage === 1
                Layout.columnSpan: 2
                Layout.fillWidth: true
                
                SectionItemValue
                {
                    id: _gross_mass_1_
                    placeholderText: "Gross Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _payload_mass_1_
                    placeholderText: "Payload Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _total_mass_1_
                    placeholderText: "Total Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _propellant_fraction_1_
                    placeholderText: "Propellant Fraction []"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _structure_fraction_1_
                    placeholderText: "Structure Fraction []"
                    readOnly: true
                }
            }

            // >>> Stage 2

            SectionItemName
            {
                text: "Structural Mass [kg]"
                visible: p_CurrentStage === 2
            }

            SectionItemValue
            {
                id: _structural_mass_2_
                visible: p_CurrentStage === 2
            }

            SectionItemName
            {
                text: "Propellant Mass [kg]"
                visible: p_CurrentStage === 2
            }

            SectionItemValue
            {
                id: _propellant_mass_2_
                visible: p_CurrentStage === 2
            }

            SectionItemName
            {
                text: "Diameter [m]"
                visible: p_CurrentStage === 2
            }

            SectionItemValue
            {
                id: _diameter_2_
                visible: p_CurrentStage === 2
            }

            GridLayout
            {
                columns: 3
                rowSpacing: 10
                columnSpacing: 10
                visible: p_CurrentStage === 2
                Layout.columnSpan: 2
                Layout.fillWidth: true
                
                SectionItemValue
                {
                    id: _gross_mass_2_
                    placeholderText: "Gross Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _payload_mass_2_
                    placeholderText: "Payload Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _total_mass_2_
                    placeholderText: "Total Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _propellant_fraction_2_
                    placeholderText: "Propellant Fraction []"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _structure_fraction_2_
                    placeholderText: "Structure Fraction []"
                    readOnly: true
                }
            }

            // >>> Stage 3

            SectionItemName
            {
                text: "Structural Mass [kg]"
                visible: p_CurrentStage === 3
            }

            SectionItemValue
            {
                id: _structural_mass_3_
                visible: p_CurrentStage === 3
            }

            SectionItemName
            {
                text: "Propellant Mass [kg]"
                visible: p_CurrentStage === 3
            }

            SectionItemValue
            {
                id: _propellant_mass_3_
                visible: p_CurrentStage === 3
            }

            SectionItemName
            {
                text: "Diameter [m]"
                visible: p_CurrentStage === 3
            }

            SectionItemValue
            {
                id: _diameter_3_
                visible: p_CurrentStage === 3
            }

            GridLayout
            {
                columns: 3
                rowSpacing: 10
                columnSpacing: 10
                visible: p_CurrentStage === 3
                Layout.columnSpan: 2
                Layout.fillWidth: true
                
                SectionItemValue
                {
                    id: _gross_mass_3_
                    placeholderText: "Gross Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _payload_mass_3_
                    placeholderText: "Payload Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _total_mass_3_
                    placeholderText: "Total Mass [kg]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _propellant_fraction_3_
                    placeholderText: "Propellant Fraction []"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _structure_fraction_3_
                    placeholderText: "Structure Fraction []"
                    readOnly: true
                }
            }

            // >>> Payload

            SectionItemName
            {
                text: "Payload Mass [kg]"
                visible: p_CurrentStage === 0
            }

            SectionItemValue
            {
                id: _payload_mass_
                visible: p_CurrentStage === 0
            }
        }

        // --- PROPULSION 

        SectionHeader
        {
            id: _propulsion_
            visible: p_CurrentStage > 0
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

            // >>> Stage 1

            SectionItemName
            {
                text: "Vacuum Specific Impulse [s]"
                visible: p_CurrentStage === 1
            }

            SectionItemValue
            {
                id: _specific_impulse_1_
                visible: p_CurrentStage === 1
            }

            SectionItemName
            {
                text: "Vacuum Thrust [N]"
                visible: p_CurrentStage === 1
            }

            SectionItemValue
            {
                id: _thrust_1_
                visible: p_CurrentStage === 1
            }

            RowLayout
            {
                spacing: 10
                visible: p_CurrentStage === 1
                Layout.columnSpan: 2
                Layout.fillWidth: true
                
                SectionItemValue
                {
                    id: _propellant_mass_flow_rate_1_
                    placeholderText: "Propellant Mass Flow Rate [kg/s]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _burn_time_1_
                    placeholderText: "Burn Time [s]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _thrust_to_weight_ratio_1_
                    placeholderText: "Thrust / Weight []"
                    readOnly: true
                }
            }

            // >>> Stage 2

            SectionItemName
            {
                text: "Vacuum Specific Impulse [s]"
                visible: p_CurrentStage === 2
            }

            SectionItemValue
            {
                id: _specific_impulse_2_
                visible: p_CurrentStage === 2
            }

            SectionItemName
            {
                text: "Vacuum Thrust [N]"
                visible: p_CurrentStage === 2
            }

            SectionItemValue
            {
                id: _thrust_2_
                visible: p_CurrentStage === 2
            }

            RowLayout
            {
                spacing: 10
                Layout.columnSpan: 2
                Layout.fillWidth: true
                visible: p_CurrentStage === 2
                
                SectionItemValue
                {
                    id: _propellant_mass_flow_rate_2_
                    placeholderText: "Propellant Mass Flow Rate [kg/s]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _burn_time_2_
                    placeholderText: "Burn Time [s]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _thrust_to_weight_ratio_2_
                    placeholderText: "Thrust / Weight []"
                    readOnly: true
                }
            }

            // >>> Stage 3

            SectionItemName
            {
                text: "Vacuum Specific Impulse [s]"
                visible: p_CurrentStage === 3
            }

            SectionItemValue
            {
                id: _specific_impulse_3_
                visible: p_CurrentStage === 3
            }

            SectionItemName
            {
                text: "Vacuum Thrust [N]"
                visible: p_CurrentStage === 3
            }

            SectionItemValue
            {
                id: _thrust_3_
                visible: p_CurrentStage === 3
            }

            RowLayout
            {
                spacing: 10
                visible: p_CurrentStage === 3
                Layout.columnSpan: 2
                Layout.fillWidth: true
                
                SectionItemValue
                {
                    id: _propellant_mass_flow_rate_3_
                    placeholderText: "Propellant Mass Flow Rate [kg/s]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _burn_time_3_
                    placeholderText: "Burn Time [s]"
                    readOnly: true
                }

                SectionItemValue
                {
                    id: _thrust_to_weight_ratio_3_
                    placeholderText: "Thrust / Weight []"
                    readOnly: true
                }
            }
        }

        // --- AERODYNAMICS 

        SectionHeader
        {
            id: _aerodynamics_
            visible: p_CurrentStage > 0
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

            // >>> Stage 1

            SectionItemName
            {
                text: "Drag Coefficient [-]"
                visible: p_CurrentStage === 1
            }

            SectionItemValue
            {
                id: _drag_coefficient_1_
                visible: p_CurrentStage === 1
            }

            SectionItemName
            {
                text: "Lift Coefficient [-]"
                visible: p_CurrentStage === 1
            }

            SectionItemValue
            {
                id: _lift_coefficient_1_
                visible: p_CurrentStage === 1
            }

            RowLayout
            {
                spacing: 10
                Layout.columnSpan: 2
                Layout.fillWidth: true
                visible: p_CurrentStage === 1
                
                SectionItemValue
                {
                    id: _reference_surface_1_
                    placeholderText: "Reference Surface [m^2]"
                    readOnly: true
                }
            }

            // >>> Stage 2

            SectionItemName
            {
                text: "Drag Coefficient [-]"
                visible: p_CurrentStage === 2
            }

            SectionItemValue
            {
                id: _drag_coefficient_2_
                visible: p_CurrentStage === 2
            }

            SectionItemName
            {
                text: "Lift Coefficient [-]"
                visible: p_CurrentStage === 2
            }

            SectionItemValue
            {
                id: _lift_coefficient_2_
                visible: p_CurrentStage === 2
            }

            RowLayout
            {
                spacing: 10
                Layout.columnSpan: 2
                Layout.fillWidth: true
                visible: p_CurrentStage === 2
                
                SectionItemValue
                {
                    id: _reference_surface_2_
                    placeholderText: "Reference Surface [m^2]"
                    readOnly: true
                }
            }

            // >>> Stage 3

            SectionItemName
            {
                text: "Drag Coefficient [-]"
                visible: p_CurrentStage === 3
            }

            SectionItemValue
            {
                id: _drag_coefficient_3_
                visible: p_CurrentStage === 3
            }

            SectionItemName
            {
                text: "Lift Coefficient [-]"
                visible: p_CurrentStage === 3
            }

            SectionItemValue
            {
                id: _lift_coefficient_3_
                visible: p_CurrentStage === 3
            }

            RowLayout
            {
                spacing: 10
                Layout.columnSpan: 2
                Layout.fillWidth: true
                visible: p_CurrentStage === 3
                
                SectionItemValue
                {
                    id: _reference_surface_3_
                    placeholderText: "Reference Surface [m^2]"
                    readOnly: true
                }
            }
        }
    }
}