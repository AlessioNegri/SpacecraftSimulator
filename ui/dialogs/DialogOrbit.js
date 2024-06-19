// ? Updates the parameters and saves based on the \a save option.
function updateParameters(save)
{
    __Orbit.body = _celestialBody_.currentIndex

    switch (_selection_.currentIndex)
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

            __Orbit.semi_major_axis                 = _a_.text
            __Orbit.eccentricity                    = _e_.text
            __Orbit.inclination                     = _i_.text
            __Orbit.right_ascension_ascending_node  = _Omega_.text
            __Orbit.periapsis_anomaly               = _omega_.text
            __Orbit.true_anomaly                    = _theta_.text

            break

        case 2: // * Modified Keplerian

            __Orbit.periapsis_radius                = _r_p_.text
            __Orbit.apoapsis_radius                 = _r_a_.text
            __Orbit.inclination                     = _i_2_.text
            __Orbit.right_ascension_ascending_node  = _Omega_2_.text
            __Orbit.periapsis_anomaly               = _omega_2_.text
            __Orbit.true_anomaly                    = _theta_2_.text

            break
        
        default:

            break
    }

    if (p_Departure)
    {
        save ? __MissionOrbitTransfer.saveDepartureOrbit() : __MissionOrbitTransfer.updateDepartureOrbit()
    }
    else
    {
        save ? __MissionOrbitTransfer.saveArrivalOrbit() : __MissionOrbitTransfer.updateArrivalOrbit()
    }

    if (save) close()
}