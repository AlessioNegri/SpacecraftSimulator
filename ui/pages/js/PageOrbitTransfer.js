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

        console.log(maneuver)

        // * Create QML component

        let component = Qt.createComponent("../../components/maneuver/ManeuverInfo.qml")

        if (component.status == Component.Ready)
        {
            var obj = component.createObject(_container_,
            {
                "p_Type"            : maneuver.type,
                "p_DeltaVelocity"   : maneuver.delta_velocity,
                "p_DeltaTime"       : maneuver.delta_time,
                "p_DeltaMass"       : maneuver.delta_mass
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
            console.error("Error loading component: " + component.errorString())
        }
    }
}