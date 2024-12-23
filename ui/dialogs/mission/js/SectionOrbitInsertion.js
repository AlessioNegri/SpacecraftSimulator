// ? Saves the parameters of the dialog.
function saveParameters()
{
    __MissionOrbitInsertion.pitchover_height                = _pitchover_height_.text
    __MissionOrbitInsertion.pitchover_flight_path_angle     = _pitchover_flight_path_angle_.text
    __MissionOrbitInsertion.circular_parking_orbit_height   = _circular_parking_orbit_height_.text

    __MissionOrbitInsertion.final_integration_time          = _final_integration_time_.text

    __MissionOrbitInsertion.use_stage_1                     = _use_stage_1_.checked
    __MissionOrbitInsertion.thrust_to_weight_ratio_1        = _thrust_to_weight_ratio_1_.text
    __MissionOrbitInsertion.average_flight_path_angle_1     = _average_flight_path_angle_1_.text
    __MissionOrbitInsertion.structure_ratio_1               = _structure_ratio_1_.text

    __MissionOrbitInsertion.use_stage_2                     = _use_stage_2_.checked
    __MissionOrbitInsertion.thrust_to_weight_ratio_2        = _thrust_to_weight_ratio_2_.text
    __MissionOrbitInsertion.average_flight_path_angle_2     = _average_flight_path_angle_2_.text
    __MissionOrbitInsertion.structure_ratio_2               = _structure_ratio_2_.text
    __MissionOrbitInsertion.burnout_time_1                  = _burnout_time_1_.text

    __MissionOrbitInsertion.use_stage_3                     = _use_stage_3_.checked
    __MissionOrbitInsertion.thrust_to_weight_ratio_3        = _thrust_to_weight_ratio_3_.text
    __MissionOrbitInsertion.average_flight_path_angle_3     = _average_flight_path_angle_3_.text
    __MissionOrbitInsertion.structure_ratio_3               = _structure_ratio_3_.text
    __MissionOrbitInsertion.burnout_time_2                  = _burnout_time_2_.text
}

// ? Restores the parameters of the dialog.
function restoreParameters()
{
    _pitchover_height_.text                 = __MissionOrbitInsertion.pitchover_height
    _pitchover_flight_path_angle_.text      = __MissionOrbitInsertion.pitchover_flight_path_angle
    _circular_parking_orbit_height_.text    = __MissionOrbitInsertion.circular_parking_orbit_height
    _circular_parking_orbit_velocity_.text  = __MissionOrbitInsertion.circular_parking_orbit_velocity

    _final_integration_time_.text           = __MissionOrbitInsertion.final_integration_time

    _use_stage_1_.checked                   = __MissionOrbitInsertion.use_stage_1
    _thrust_to_weight_ratio_1_.text         = __MissionOrbitInsertion.thrust_to_weight_ratio_1
    _average_flight_path_angle_1_.text      = __MissionOrbitInsertion.average_flight_path_angle_1
    _structure_ratio_1_.text                = __MissionOrbitInsertion.structure_ratio_1

    _use_stage_2_.checked                   = __MissionOrbitInsertion.use_stage_2
    _thrust_to_weight_ratio_2_.text         = __MissionOrbitInsertion.thrust_to_weight_ratio_2
    _average_flight_path_angle_2_.text      = __MissionOrbitInsertion.average_flight_path_angle_2
    _structure_ratio_2_.text                = __MissionOrbitInsertion.structure_ratio_2
    _burnout_time_1_.text                   = __MissionOrbitInsertion.burnout_time_1

    _use_stage_3_.checked                   = __MissionOrbitInsertion.use_stage_3
    _thrust_to_weight_ratio_3_.text         = __MissionOrbitInsertion.thrust_to_weight_ratio_3
    _average_flight_path_angle_3_.text      = __MissionOrbitInsertion.average_flight_path_angle_3
    _structure_ratio_3_.text                = __MissionOrbitInsertion.structure_ratio_3
    _burnout_time_2_.text                   = __MissionOrbitInsertion.burnout_time_2
}