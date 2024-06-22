// ? Updates the parameters of the orbital perturbations transfer.
function saveParameters()
{
    __MissionOrbitPropagation.angular_momentum                  = _h_.text
    __MissionOrbitPropagation.eccentricity                      = _e_.text
    __MissionOrbitPropagation.inclination                       = _i_.text
    __MissionOrbitPropagation.right_ascension_ascending_node    = _Omega_.text
    __MissionOrbitPropagation.periapsis_anomaly                 = _omega_.text
    __MissionOrbitPropagation.true_anomaly                      = _theta_.text

    __MissionOrbitPropagation.drag                              = _drag_.checked
    __MissionOrbitPropagation.drag_ballistic_coefficient        = _B_.text
    __MissionOrbitPropagation.gravitational                     = _gravitational_.checked
    __MissionOrbitPropagation.srp                               = _srp_.checked
    __MissionOrbitPropagation.srp_ballistic_coefficient         = _B_SRP_.text
    __MissionOrbitPropagation.third_body                        = _third_body_.checked
    __MissionOrbitPropagation.third_body_choice                 = _third_body_combo_box_.currentIndex
    __MissionOrbitPropagation.start_date                        = _start_date.displayText
    __MissionOrbitPropagation.end_date                          = _end_date_.displayText

    __MissionOrbitPropagation.saveOrbitalPerturbationsParameters()
}