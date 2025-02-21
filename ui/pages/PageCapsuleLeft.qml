import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageCapsuleLeft.js" as Script

import "../components/common"
import "../components/material"

// * The PageCapsuleLeft class manages the capsule left page.
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

        // --- STRUCTURE 

        SectionHeader
        {
            id: _capsule_
            p_Title: "Structure"
            p_Icon: "/png/structure.png"
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 20
            columnSpacing: 20
            visible: !_capsule_.p_Hide
            Layout.fillWidth: true

            SectionItemName
            {
                text: "Mass [kg]"
            }

            SectionItemValue
            {
                id: _capsule_mass_
            }

            SectionItemName
            {
                text: "Nose Radius [m]"
            }

            SectionItemValue
            {
                id: _capsule_nose_radius_
            }

            SectionItemName
            {
                text: "Body Radius [m]"
            }

            SectionItemValue
            {
                id: _capsule_body_radius_
            }

            SectionItemName
            {
                text: "Shield Angle [deg]"
            }

            SectionItemValue
            {
                id: _capsule_shield_angle_
            }

            SectionItemName
            {
                text: "Afterbody Angle [deg]"
            }

            SectionItemValue
            {
                id: _capsule_afterbody_angle_
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
                text: "Specific Heat Ratio [-]"
            }

            SectionItemValue
            {
                id: _specific_heat_ratio_
            }

            SectionItemName
            {
                text: "Zero-Lift Drag Coefficient [-]"
            }

            SectionItemValue
            {
                id: _capsule_zero_lift_drag_coefficient_
            }

            SectionItemName
            {
                text: "Lift Coefficient [-]"
            }

            SectionItemValue
            {
                id: _capsule_lift_coefficient_
            }

            SectionItemName
            {
                text: "Drag Coefficient [-]"
            }

            SectionItemValue
            {
                id: _capsule_drag_coefficient_
            }

            SectionItemName
            {
                text: "Reference Surface [m^2]"
            }

            SectionItemValue
            {
                id: _capsule_reference_surface_
            }
                
            SectionItemName
            {
                text: "Angle Of Attack [deg]"
            }

            RowLayout
            {
                spacing: 10

                SectionItemValue
                {
                    id: _capsule_angle_of_attack_
                }

                MaterialButton
                {
                    text: "Update Coefficients"

                    onClicked:
                    {
                        __Capsule.capsule_angle_of_attack = _capsule_angle_of_attack_.text

                        __Capsule.update_coefficients()

                        Script.reloadAerodynamicCoefficients()

                        notification_text.text = "Aerodynamic Coefficients Updated"
                                
                        notification.start()
                    }
                }
            }
        }

        // --- PARACHUTE 

        SectionHeader
        {
            id: _parachute_
            p_Title: "Parachute"
            p_Icon: "/png/parachute.png"
        }

        GridLayout
        {
            columns: 2
            rowSpacing: 20
            columnSpacing: 20
            visible: !_parachute_.p_Hide
            Layout.fillWidth: true

            SectionItemName
            {
                text: "Drag Coefficient [-]"
            }

            SectionItemValue
            {
                id: _parachute_drag_coefficient_
            }

            SectionItemName
            {
                text: "Reference Surface [m^2]"
            }

            SectionItemValue
            {
                id: _parachute_reference_surface_
            }
        }
    }
}