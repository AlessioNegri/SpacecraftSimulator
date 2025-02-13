import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/common"
import "../components/dialog"
import "../components/material"

// * The DialogAbout class manages the about dialog.
Dialog
{
    // * Loads all the parameters.
    function load()
    {
        _flare_height_ratio_.text       = __MissionOrbitInsertion.flare_height_ratio
        _flare_surface_ratio_.text      = __MissionOrbitInsertion.flare_surface_ratio
        _afterbody_height_ratio_.text   = __MissionOrbitInsertion.afterbody_height_ratio
        _fin_correction_factor_.text    = __MissionOrbitInsertion.fin_correction_factor
    }

    // * Saves all the parameters.
    function save()
    {
        __MissionOrbitInsertion.flare_height_ratio      = _flare_height_ratio_.text 
        __MissionOrbitInsertion.flare_surface_ratio     = _flare_surface_ratio_.text
        __MissionOrbitInsertion.afterbody_height_ratio  = _afterbody_height_ratio_.text
        __MissionOrbitInsertion.fin_correction_factor   = _fin_correction_factor_.text

        load()
    }

    // ! ----------------------------------------- ! //
    
    id: root
    title: "Launcher Details"
    anchors.centerIn: parent
    modal: true
    font.pointSize: 12
    width: parent.width
    height: parent.height
    closePolicy: Popup.NoAutoClose

    onVisibleChanged:
    {
        if (visible)
        {
            load()

            let w = _image_.width
            let l = __MissionOrbitInsertion.launcher_length

            _stage_1_h_cg_.anchors.rightMargin  = w * __MissionOrbitInsertion.stage_1.stage_center_of_gravity_height / l
            _stage_2_h_cg_.anchors.rightMargin  = w * __MissionOrbitInsertion.stage_2.stage_center_of_gravity_height / l
            _frustum_h_cg_.anchors.rightMargin  = w * __MissionOrbitInsertion.frustum.stage_center_of_gravity_height / l
            _stage_3_h_cg_.anchors.rightMargin  = w * __MissionOrbitInsertion.stage_3.stage_center_of_gravity_height / l
            _payload_h_cg_.anchors.rightMargin  = w * __MissionOrbitInsertion.payload.stage_center_of_gravity_height / l
            _stack_h_cg_.anchors.rightMargin    = w * __MissionOrbitInsertion.stack_I_center_of_gravity_height / l
            _cp_.anchors.leftMargin             = w * __MissionOrbitInsertion.center_of_pressure / l
        }
    }

    background: Rectangle
    {
        color: "#162A35"
        radius: 10
        border.width: 2
        border.color: "#93F9D8"
    }

    header: DialogHeader
    {
        p_Title: "Launcher Details"

        function f_Close()
        {
            close()
        }
    }

    contentItem: Item
    {
        ColumnLayout
        {
            spacing: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 10

            RowLayout
            {
                spacing: 10
                
                SectionItemValue
                {
                    id: _flare_height_ratio_
                    placeholderText: "Flare Height Ratio"
                }

                SectionItemValue
                {
                    id: _flare_surface_ratio_
                    placeholderText: "Flare Surface Ratio"
                }

                SectionItemValue
                {
                    id: _afterbody_height_ratio_
                    placeholderText: "Afterbody height ratio"
                }

                SectionItemValue
                {
                    id: _fin_correction_factor_
                    placeholderText: "Fin Correction Factor"
                }

                MaterialButton
                {
                    text: "Update"
                    onClicked:
                    {
                        save()

                        __MissionOrbitInsertion.update_center_of_pressure()

                        let w = _image_.width
                        let l = __MissionOrbitInsertion.launcher_length

                        _cp_.anchors.leftMargin = w * __MissionOrbitInsertion.center_of_pressure / l
                    }
                }
            }

            RowLayout
            {
                spacing: 10

                Image
                {
                    source: "/png/center_of_gravity.png"
                    sourceSize.width: 30
                    sourceSize.height: 30
                    fillMode: Image.PreserveAspectFit
                }

                Text
                {
                    text: "Element Center Of Gravity"
                    color: "#FFFFFF"
                    font.bold: true
                }

                Image
                {
                    source: "/png/center_of_gravity.png"
                    sourceSize.width: 50
                    sourceSize.height: 50
                    fillMode: Image.PreserveAspectFit
                }

                Text
                {
                    text: "Launcher Center Of Gravity"
                    color: "#FFFFFF"
                    font.bold: true
                }

                Image
                {
                    source: "/png/center_of_pressure.png"
                    sourceSize.width: 50
                    sourceSize.height: 50
                    fillMode: Image.PreserveAspectFit
                }

                Text
                {
                    text: "Launcher Center Of Pressure"
                    color: "#FFFFFF"
                    font.bold: true
                }
            }
        }
        

        Image
        {
            id: _image_
            source: "/png/launcher_full.png"
            sourceSize.width: parent.width
            fillMode: Image.PreserveAspectFit
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 10

            Image
            {
                id: _stage_1_h_cg_
                source: "/png/center_of_gravity.png"
                sourceSize.width: 30
                sourceSize.height: 30
                fillMode: Image.PreserveAspectFit
                anchors.right: parent.right
                anchors.verticalCenter: _image_.verticalCenter
            }

            Image
            {
                id: _stage_2_h_cg_
                source: "/png/center_of_gravity.png"
                sourceSize.width: 30
                sourceSize.height: 30
                fillMode: Image.PreserveAspectFit
                anchors.right: parent.right
                anchors.verticalCenter: _image_.verticalCenter
            }

            Image
            {
                id: _frustum_h_cg_
                source: "/png/center_of_gravity.png"
                sourceSize.width: 30
                sourceSize.height: 30
                fillMode: Image.PreserveAspectFit
                anchors.right: parent.right
                anchors.verticalCenter: _image_.verticalCenter
            }

            Image
            {
                id: _stage_3_h_cg_
                source: "/png/center_of_gravity.png"
                sourceSize.width: 30
                sourceSize.height: 30
                fillMode: Image.PreserveAspectFit
                anchors.right: parent.right
                anchors.verticalCenter: _image_.verticalCenter
            }

            Image
            {
                id: _payload_h_cg_
                source: "/png/center_of_gravity.png"
                sourceSize.width: 30
                sourceSize.height: 30
                fillMode: Image.PreserveAspectFit
                anchors.right: parent.right
                anchors.verticalCenter: _image_.verticalCenter
            }

            Image
            {
                id: _stack_h_cg_
                source: "/png/center_of_gravity.png"
                sourceSize.width: 50
                sourceSize.height: 50
                fillMode: Image.PreserveAspectFit
                anchors.right: parent.right
                anchors.verticalCenter: _image_.verticalCenter
            }

            Image
            {
                id: _cp_
                source: "/png/center_of_pressure.png"
                sourceSize.width: 50
                sourceSize.height: 50
                fillMode: Image.PreserveAspectFit
                anchors.left: parent.left
                anchors.verticalCenter: _image_.verticalCenter
            }
        }
    }
}