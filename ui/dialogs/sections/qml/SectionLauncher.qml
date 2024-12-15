import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../../components"

import "../js/SectionLauncher.js" as Script

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

    width: parent.width
    contentWidth: parent.width
    contentHeight: _layout_.height
    onVisibleChanged: if (visible) load()

    ColumnLayout
    {
        id: _layout_
        width: parent.width - 20
        spacing: 20

        RowLayout
        {
            id: _menu_
            Layout.fillWidth: true
            spacing: 0

            SettingsMenuItem
            {
                p_Icon: "/png/stage.png"
                p_Text: "Stage 1"
                p_Selected: p_CurrentStage === 1
                Layout.fillWidth: true
                
                function f_Click() { p_CurrentStage = 1 }
            }

            SettingsMenuItem
            {
                p_Icon: "/png/stage.png"
                p_Text: "Stage 2"
                p_Selected: p_CurrentStage === 2
                Layout.fillWidth: true
                
                function f_Click() { p_CurrentStage = 2 }
            }

            SettingsMenuItem
            {
                p_Icon: "/png/stage.png"
                p_Text: "Stage 3"
                p_Selected: p_CurrentStage === 3
                Layout.fillWidth: true
                
                function f_Click() { p_CurrentStage = 3 }
            }

            SettingsMenuItem
            {
                p_Icon: "/png/payload.png"
                p_Text: "Payload"
                p_Selected: p_CurrentStage === 4
                Layout.fillWidth: true
                
                function f_Click() { p_CurrentStage = 4 }
            }
        }

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

            RowLayout
            {
                spacing: 10
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

            RowLayout
            {
                spacing: 10
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

            RowLayout
            {
                spacing: 10
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
            }

            // >>> Payload

            SectionItemName
            {
                text: "Payload Mass [kg]"
                visible: p_CurrentStage === 4
            }

            SectionItemValue
            {
                id: _payload_mass_
                visible: p_CurrentStage === 4
            }
        }

        // --- PROPULSION 

        SectionHeader
        {
            id: _propulsion_
            visible: p_CurrentStage <= 3
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
            }
        }

        // --- AERODYNAMICS 

        SectionHeader
        {
            id: _aerodynamics_
            visible: p_CurrentStage <= 3
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