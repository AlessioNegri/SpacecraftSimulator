// ? Updates the check box status for each mission, based on the one selected
function missionChanged(mission)
{
    gp_CurrentMission = mission

    _view_.setCurrentIndex(mission)

    _orbitTransferCheckBox_.checked             = mission === 0
    _orbitPropagationCheckBox_.checked          = mission === 1
    _interplanetaryTransferCheckBox_.checked    = mission === 2
    _atmosphericEntryCheckBox_.checked          = mission === 3
}