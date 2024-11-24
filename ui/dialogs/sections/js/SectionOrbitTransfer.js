// ? Updates the celestial body.
function saveCelestialBody()
{
    __Orbit.body = p_SelectedCelestialBody

    __MissionOrbitTransfer.update_celestial_body()
}

// ? Updates the parameters of the departure orbit.
function saveDepartureParameters()
{
    __Orbit.state = p_SelectedDepartureSateRepresentation

    switch (p_SelectedDepartureSateRepresentation)
    {
        case 0: // * Cartesian

            __Orbit.r_x = _departure_x_.text
            __Orbit.r_y = _departure_y_.text
            __Orbit.r_z = _departure_z_.text
            __Orbit.v_x = _departure_v_x_.text
            __Orbit.v_y = _departure_v_y_.text
            __Orbit.v_z = _departure_v_z_.text

            break

        case 1: // * Keplerian

            __Orbit.semi_major_axis                 = _departure_semi_major_axis_.text
            __Orbit.eccentricity                    = _departure_eccentricity_.text
            __Orbit.inclination                     = _departure_inclination_.text
            __Orbit.right_ascension_ascending_node  = _departure_raan_.text
            __Orbit.periapsis_anomaly               = _departure_periapsis_anomaly_.text
            __Orbit.true_anomaly                    = _departure_true_anomaly_.text

            break

        case 2: // * Modified Keplerian

            __Orbit.periapsis_radius                = _departure_periapsis_radius_.text
            __Orbit.apoapsis_radius                 = _departure_apoapsis_radius_.text
            __Orbit.inclination                     = _departure_inclination_2_.text
            __Orbit.right_ascension_ascending_node  = _departure_raan_2_.text
            __Orbit.periapsis_anomaly               = _departure_periapsis_anomaly_2_.text
            __Orbit.true_anomaly                    = _departure_true_anomaly_2_.text

            break
        
        default:

            break
    }

    __MissionOrbitTransfer.update_departure_orbit()
}

// ? Updates the parameters of the arrival orbit.
function saveArrivalParameters()
{
    __Orbit.state = p_SelectedArrivalSateRepresentation

    switch (p_SelectedArrivalSateRepresentation)
    {
        case 0: // * Cartesian

            __Orbit.r_x = _arrival_x_.text
            __Orbit.r_y = _arrival_y_.text
            __Orbit.r_z = _arrival_z_.text
            __Orbit.v_x = _arrival_v_x_.text
            __Orbit.v_y = _arrival_v_y_.text
            __Orbit.v_z = _arrival_v_z_.text

            break

        case 1: // * Keplerian

            __Orbit.semi_major_axis                 = _arrival_semi_major_axis_.text
            __Orbit.eccentricity                    = _arrival_eccentricity_.text
            __Orbit.inclination                     = _arrival_inclination_.text
            __Orbit.right_ascension_ascending_node  = _arrival_raan_.text
            __Orbit.periapsis_anomaly               = _arrival_periapsis_anomaly_.text
            __Orbit.true_anomaly                    = _arrival_true_anomaly_.text

            break

        case 2: // * Modified Keplerian

            __Orbit.periapsis_radius                = _arrival_periapsis_radius_.text
            __Orbit.apoapsis_radius                 = _arrival_apoapsis_radius_.text
            __Orbit.inclination                     = _arrival_inclination_2_.text
            __Orbit.right_ascension_ascending_node  = _arrival_raan_2_.text
            __Orbit.periapsis_anomaly               = _arrival_periapsis_anomaly_2_.text
            __Orbit.true_anomaly                    = _arrival_true_anomaly_2_.text

            break
        
        default:

            break
    }

    __MissionOrbitTransfer.update_arrival_orbit()
}

// ? Restores the parameters of the departure orbit.
function restoreDepartureParameters()
{
    p_SelectedCelestialBody                 = __Orbit.body
    p_SelectedDepartureSateRepresentation   = __Orbit.state
    _departure_x_.text                      = __Orbit.r_x
    _departure_y_.text                      = __Orbit.r_y
    _departure_z_.text                      = __Orbit.r_z
    _departure_v_x_.text                    = __Orbit.v_x
    _departure_v_y_.text                    = __Orbit.v_y
    _departure_v_z_.text                    = __Orbit.v_z
    _departure_semi_major_axis_.text        = __Orbit.semi_major_axis
    _departure_eccentricity_.text           = __Orbit.eccentricity
    _departure_inclination_.text            = __Orbit.inclination
    _departure_raan_.text                   = __Orbit.right_ascension_ascending_node
    _departure_periapsis_anomaly_.text      = __Orbit.periapsis_anomaly
    _departure_true_anomaly_.text           = __Orbit.true_anomaly
    _departure_periapsis_radius_.text       = __Orbit.periapsis_radius
    _departure_apoapsis_radius_.text        = __Orbit.apoapsis_radius
    _departure_inclination_2_.text          = __Orbit.inclination
    _departure_raan_2_.text                 = __Orbit.right_ascension_ascending_node
    _departure_periapsis_anomaly_2_.text    = __Orbit.periapsis_anomaly
    _departure_true_anomaly_2_.text         = __Orbit.true_anomaly
}

// ? Restores the parameters of the arrival orbit.
function restoreArrivalParameters()
{
    p_SelectedCelestialBody                 = __Orbit.body
    p_SelectedArrivalSateRepresentation     = __Orbit.state
    _arrival_x_.text                        = __Orbit.r_x
    _arrival_y_.text                        = __Orbit.r_y
    _arrival_z_.text                        = __Orbit.r_z
    _arrival_v_x_.text                      = __Orbit.v_x
    _arrival_v_y_.text                      = __Orbit.v_y
    _arrival_v_z_.text                      = __Orbit.v_z
    _arrival_semi_major_axis_.text          = __Orbit.semi_major_axis
    _arrival_eccentricity_.text             = __Orbit.eccentricity
    _arrival_inclination_.text              = __Orbit.inclination
    _arrival_raan_.text                     = __Orbit.right_ascension_ascending_node
    _arrival_periapsis_anomaly_.text        = __Orbit.periapsis_anomaly
    _arrival_true_anomaly_.text             = __Orbit.true_anomaly
    _arrival_periapsis_radius_.text         = __Orbit.periapsis_radius
    _arrival_apoapsis_radius_.text          = __Orbit.apoapsis_radius
    _arrival_inclination_2_.text            = __Orbit.inclination
    _arrival_raan_2_.text                   = __Orbit.right_ascension_ascending_node
    _arrival_periapsis_anomaly_2_.text      = __Orbit.periapsis_anomaly
    _arrival_true_anomaly_2_.text           = __Orbit.true_anomaly
}

// ? Clears the maneuvers.
function clearManeuvers()
{
    for (let i = r_Maneuvers.length - 1; i >= 0; --i)
    {
        r_Maneuvers[i].destroy()

        r_Maneuvers.pop()
    }
}

// ? Loads the maneuvers from the backend.
function loadManeuvers()
{
    // * Clear

    clearManeuvers()

    // * Cycle

    let len = __MissionOrbitTransfer.maneuver_count()

    for (let i = 0; i < len; ++i)
    {
        // * Retrieve maneuver from backend

        var maneuver = __MissionOrbitTransfer.maneuver(i)

        // * Create QML component

        let component = Qt.createComponent("../../../components/Maneuver.qml")

        if (component.status == Component.Ready)
        {
            var obj = component.createObject(_container_,
            {
                "p_Id"              : r_Maneuvers.length + 1,
                "p_Type"            : maneuver.type,
                "p_Option"          : maneuver.option,
                "p_OptionValue"     : maneuver.option_value
            })
            
            if (obj == null)
            {
                console.log("Error creating object")

                continue
            }

            // * Add and update

            r_Maneuvers.push(obj)
        }
        else if (component.status == Component.Error)
        {
            console.error("Error loading component:" + component.errorString())
        }
    }
}

// ? Adds a new maneuver.
function addManeuver()
{
    // * Create QML component

    let component = Qt.createComponent("../../../components/Maneuver.qml")

    if (component.status == Component.Ready)
    {
        var obj = component.createObject(_container_, { "p_Id": r_Maneuvers.length + 1 })
        
        if (obj == null)
        {
            console.log("Error creating object")
        }

        // * Add and update

        r_Maneuvers.push(obj)
    }
    else if (component.status == Component.Error)
    {
        console.error("Error loading component:" + component.errorString())
    }
}

// ? Removes the maneuvers with the given Id.
function removeManeuver(id)
{
    for (let i = 0; i < r_Maneuvers.length; ++i)
    {
        if (r_Maneuvers[i].p_Id === id)
        {
            r_Maneuvers[i].destroy()

            r_Maneuvers.splice(i, 1)

            break
        }
    }
}

// ? Updates the maneuvers in the backend.
function saveManeuvers()
{
    __MissionOrbitTransfer.clear_maneuvers()

    for (let i = 0; i < r_Maneuvers.length; ++i)
    {
        __MissionOrbitTransfer.add_maneuver(r_Maneuvers[i].p_Type, r_Maneuvers[i].p_Option, r_Maneuvers[i].p_OptionValue)
    }
}