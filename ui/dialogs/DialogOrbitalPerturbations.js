// ? Updates the parameters of the orbital perturbations.
function saveParameters()
{
    __MissionOrbitPropagation.angular_momentum                  = _angular_momentum_.text
    __MissionOrbitPropagation.eccentricity                      = _eccentricity_.text
    __MissionOrbitPropagation.inclination                       = _inclination_.text
    __MissionOrbitPropagation.right_ascension_ascending_node    = _raan_.text
    __MissionOrbitPropagation.periapsis_anomaly                 = _periapsis_anomaly_.text
    __MissionOrbitPropagation.true_anomaly                      = _true_anomaly_.text

    __MissionOrbitPropagation.drag                              = _drag_.checked
    __MissionOrbitPropagation.gravitational                     = _gravitational_.checked
    __MissionOrbitPropagation.solar_radiation_pressure          = _solar_radiation_pressure_.checked
    __MissionOrbitPropagation.third_body                        = _third_body_.checked
    __MissionOrbitPropagation.third_body_choice                 = _third_body_combo_box_.currentIndex
    __MissionOrbitPropagation.start_date                        = _start_date_.displayText
    __MissionOrbitPropagation.end_date                          = _end_date_.displayText
}

// ? Restores the parameters of the spacecraft.
function restoreParameters()
{
    _angular_momentum_.text             = __MissionOrbitPropagation.angular_momentum
    _eccentricity_.text                 = __MissionOrbitPropagation.eccentricity
    _inclination_.text                  = __MissionOrbitPropagation.inclination
    _raan_.text                         = __MissionOrbitPropagation.right_ascension_ascending_node
    _periapsis_anomaly_.text            = __MissionOrbitPropagation.periapsis_anomaly
    _true_anomaly_.text                 = __MissionOrbitPropagation.true_anomaly

    _drag_.checked                      = __MissionOrbitPropagation.drag
    _gravitational_.checked             = __MissionOrbitPropagation.gravitational
    _solar_radiation_pressure_.checked  = __MissionOrbitPropagation.solar_radiation_pressure
    _third_body_.checked                = __MissionOrbitPropagation.third_body
    _third_body_combo_box_.currentIndex = __MissionOrbitPropagation.third_body_choice
    _start_date_.text                   = __MissionOrbitPropagation.start_date
    _end_date_.text                     = __MissionOrbitPropagation.end_date
}