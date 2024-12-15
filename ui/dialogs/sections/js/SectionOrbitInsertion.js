// >>> Saves the parameters of the dialog.
function saveParameters()
{
    __MissionOrbitInsertion.pitchover_height            = _pitchover_height_.text
    __MissionOrbitInsertion.pitchover_flight_path_angle = _pitchover_flight_path_angle_.text
    __MissionOrbitInsertion.final_integration_time      = _final_integration_time_.text
}

// >>> Restores the parameters of the dialog.
function restoreParameters()
{
    _pitchover_height_.text             = __MissionOrbitInsertion.pitchover_height
    _pitchover_flight_path_angle_.text  = __MissionOrbitInsertion.pitchover_flight_path_angle
    _final_integration_time_.text       = __MissionOrbitInsertion.final_integration_time
}