import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/common"
import "../components/dialog"
import "../components/material"

import "PageLauncherLeft"

// * The PageLauncherLeft class manages the launcher left poge.
ScrollView
{
    // * Selected stage.
    property int p_CurrentStage: 1

    // * Loads all the parameters.
    function load()
    {
        _stage_1_.load()
        _stage_2_.load()
        _frustum_.load()
        _stage_3_.load()
        _payload_.load()
    }

    // * Saves all the parameters.
    function save()
    {
        _stage_1_.save()
        _stage_2_.save()
        _frustum_.save()
        _stage_3_.save()
        _payload_.save()

        __MissionOrbitInsertion.connect_stages()
        
        load()
    }

    // ! ----------------------------------------- ! //

    Component.onCompleted: load()

    width: parent.width - 20
    contentWidth: parent.width
    contentHeight: _stage_1_.height

    ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }
    ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }

    onP_CurrentStageChanged:
    {
        switch (p_CurrentStage)
        {
            case  1: contentHeight = _stage_1_.height; break;
            case  2: contentHeight = _stage_2_.height; break;
            case -1: contentHeight = _frustum_.height; break;
            case  3: contentHeight = _stage_3_.height; break;
            case  0: contentHeight = _payload_.height; break;
        }

        return 0
    }

    Stage1
    {
        id: _stage_1_
        visible: p_CurrentStage === 1
    }

    Stage2
    {
        id: _stage_2_
        visible: p_CurrentStage === 2
    }

    Frustum
    {
        id: _frustum_
        visible: p_CurrentStage === -1
    }

    Stage3
    {
        id: _stage_3_
        visible: p_CurrentStage === 3
    }

    Payload
    {
        id: _payload_
        visible: p_CurrentStage === 0
    }
}