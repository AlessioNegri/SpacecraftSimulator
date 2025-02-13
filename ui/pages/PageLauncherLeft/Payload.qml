import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../components/common"
import "../../components/dialog"
import "../../components/material"

// * The Payload class manages the launcher left poge payload.
ColumnLayout
{
    // * Loads all the parameters.
    function load()
    {
        // ? Mass

        _payload_mass_.text = __MissionOrbitInsertion.payload.payload_mass

        // ? Geometry

        _diameter_.text     = __MissionOrbitInsertion.payload.diameter
        _height_.text       = __MissionOrbitInsertion.payload.height
        _cog_height_.text   = __MissionOrbitInsertion.payload.stage_center_of_gravity_height
        _moi_.text          = __MissionOrbitInsertion.payload.stage_moment_of_inertia
    }

    // * Saves all the parameters.
    function save()
    {
        // ? Mass

        __MissionOrbitInsertion.payload.payload_mass    = _payload_mass_.text
        
        // ? Geometry

        __MissionOrbitInsertion.payload.diameter        = _diameter_.text
        __MissionOrbitInsertion.payload.height          = _height_.text

        load()
    }

    // ! ----------------------------------------- ! //

    id: _layout_
    width: parent.width - 20
    spacing: 20

    // --- MASS 

    SectionItemName
    {
        text: "Payload Mass [kg]"
    }

    SectionItemValue
    {
        id: _payload_mass_
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
            text: "Base Diameter [m]"
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
                id: _cog_height_
                placeholderText: "Center Of Gravity Height [m]"
                readOnly: true
            }

            SectionItemValue
            {
                id: _moi_
                placeholderText: "Moment Of Inertia [kg * m^2]"
                readOnly: true
            }
        }
    }
}