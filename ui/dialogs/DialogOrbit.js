// ? Updates the parameters of the orbit.
function saveParameters()
{
    __Orbit.body    = _celestial_body_.currentIndex
    __Orbit.state   = _representation_.currentIndex

    switch (_representation_.currentIndex)
    {
        case 0: // * Cartesian

            __Orbit.r_x = _x_.text
            __Orbit.r_y = _y_.text
            __Orbit.r_z = _z_.text
            __Orbit.v_x = _v_x_.text
            __Orbit.v_y = _v_y_.text
            __Orbit.v_z = _v_z_.text

            break

        case 1: // * Keplerian

            __Orbit.semi_major_axis                 = _semi_major_axis_.text
            __Orbit.eccentricity                    = _eccentricity_.text
            __Orbit.inclination                     = _inclination_.text
            __Orbit.right_ascension_ascending_node  = _raan_.text
            __Orbit.periapsis_anomaly               = _periapsis_anomaly_.text
            __Orbit.true_anomaly                    = _true_anomaly_.text

            break

        case 2: // * Modified Keplerian

            __Orbit.periapsis_radius                = _periapsis_radius_.text
            __Orbit.apoapsis_radius                 = _apoapsis_radius_.text
            __Orbit.inclination                     = _inclination_2_.text
            __Orbit.right_ascension_ascending_node  = _raan_2_.text
            __Orbit.periapsis_anomaly               = _periapsis_anomaly_2_.text
            __Orbit.true_anomaly                    = _true_anomaly_2_.text

            break
        
        default:

            break
    }

    if (p_Departure)
    {
        __MissionOrbitTransfer.update_departure_orbit()
    }
    else
    {
        __MissionOrbitTransfer.update_arrival_orbit()
    }

    restoreParameters()
}

// ? Restores the parameters of the orbit.
function restoreParameters()
{
    _celestial_body_.currentIndex   = __Orbit.body
    _representation_.currentIndex   = __Orbit.state
    _x_.text                        = __Orbit.r_x
    _y_.text                        = __Orbit.r_y
    _z_.text                        = __Orbit.r_z
    _v_x_.text                      = __Orbit.v_x
    _v_y_.text                      = __Orbit.v_y
    _v_z_.text                      = __Orbit.v_z
    _semi_major_axis_.text          = __Orbit.semi_major_axis
    _eccentricity_.text             = __Orbit.eccentricity
    _inclination_.text              = __Orbit.inclination
    _raan_.text                     = __Orbit.right_ascension_ascending_node
    _periapsis_anomaly_.text        = __Orbit.periapsis_anomaly
    _true_anomaly_.text             = __Orbit.true_anomaly
    _periapsis_radius_.text         = __Orbit.periapsis_radius
    _apoapsis_radius_.text          = __Orbit.apoapsis_radius
    _inclination_2_.text            = __Orbit.inclination
    _raan_2_.text                   = __Orbit.right_ascension_ascending_node
    _periapsis_anomaly_2_.text      = __Orbit.periapsis_anomaly
    _true_anomaly_2_.text           = __Orbit.true_anomaly
}