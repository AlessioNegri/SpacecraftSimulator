// ? Saves the parameters of the dialog.
function saveParameters()
{
    __MissionAtmosphericEntry.entry_velocity            = _entry_velocity_.text
    __MissionAtmosphericEntry.entry_flight_path_angle   = _entry_flight_path_angle_.text
    __MissionAtmosphericEntry.entry_altitude            = _entry_altitude_.text
    __MissionAtmosphericEntry.final_integration_time    = _final_integration_time_.text
    __MissionAtmosphericEntry.use_parachute             = _use_parachute_.checked
}

// ? Restores the parameters of the dialog.
function restoreParameters()
{
    _entry_velocity_.text           = __MissionAtmosphericEntry.entry_velocity
    _entry_flight_path_angle_.text  = __MissionAtmosphericEntry.entry_flight_path_angle
    _entry_altitude_.text           = __MissionAtmosphericEntry.entry_altitude
    _final_integration_time_.text   = __MissionAtmosphericEntry.final_integration_time
    _use_parachute_.checked         = __MissionAtmosphericEntry.use_parachute
    //_impact_velocity.text           = __MissionAtmosphericEntry.impact_velocity
}