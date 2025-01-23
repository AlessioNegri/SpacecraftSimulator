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
                id: _capsule_node_radius_
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